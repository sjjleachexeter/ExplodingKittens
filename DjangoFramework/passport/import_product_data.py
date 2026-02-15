import pandas as pd
import uuid
from datetime import date

from passport.models import (
    Product,
    Ingredient,
    ProductIngredient,
    Node,
    Stage,
    Evidence,
    Claim,
    ClaimEvidence,
)

# define csv file locations
csv_products = "data/products.csv"
csv_ingredients = "data/ingredients.csv"
csv_product_ingredients = "data/product_ingredients.csv"
csv_nodes = "data/nodes.csv"
csv_stages = "data/stages.csv"
csv_evidence = "data/evidence.csv"
csv_claims = "data/claims.csv"
csv_claim_evidence = "data/claim_evidence.csv"

# UUIDv5 helpers
NAMESPACE = uuid.NAMESPACE_URL

def u5(text: str) -> str:
    return str(uuid.uuid5(NAMESPACE, text))

def s(v) -> str:
    return "" if pd.isna(v) else str(v).strip()


def load_csv_products():
    df = pd.read_csv(csv_products)

    for index, row in df.iterrows():
        product_uuid = u5(s(row["product_id"]) + s(row["name"]))

        Product.objects.update_or_create(
            product_uuid=product_uuid,
            defaults={
                "product_id": s(row["product_id"]),
                "name": s(row["name"]),
                "category": s(row["category"]),
                "description": s(row.get("description")),
                "qr_token": s(row["qr_token"]),
            },
        )


def load_csv_ingredients():
    df = pd.read_csv(csv_ingredients)

    for index, row in df.iterrows():
        ingredient_uuid = u5(s(row["ingredient_id"]) + s(row["name"]))

        Ingredient.objects.update_or_create(
            ingredient_uuid=ingredient_uuid,
            defaults={
                "ingredient_id": s(row["ingredient_id"]),
                "name": s(row["name"]),
            },
        )


def load_csv_nodes():
    df = pd.read_csv(csv_nodes)

    for index, row in df.iterrows():
        node_uuid = u5(s(row["node_id"]) + s(row["org_name"]))

        Node.objects.update_or_create(
            node_uuid=node_uuid,
            defaults={
                "node_id": s(row["node_id"]),
                "org_name": s(row["org_name"]),
                "role": s(row["role"]),
                "country": s(row["country"]),
                "city": s(row.get("city")),
            },
        )


def load_csv_stages():
    df = pd.read_csv(csv_stages)

    for index, row in df.iterrows():
        product_uuid = Product.objects.get(product_id=s(row["product_id"])).product_uuid
        from_node_uuid = Node.objects.get(node_id=s(row["from_node_id"])).node_uuid
        to_node_uuid = Node.objects.get(node_id=s(row["to_node_id"])).node_uuid

        stage_uuid = u5(s(row["stage_id"]) + s(row["sequence"]) + s(row["stage_name"]))

        Stage.objects.update_or_create(
            stage_uuid=stage_uuid,
            defaults={
                "stage_id": s(row["stage_id"]),
                "product_uuid": product_uuid,
                "sequence": int(row["sequence"]),
                "stage_name": s(row["stage_name"]),
                "from_node": from_node_uuid,
                "to_node": to_node_uuid,
                "value_share": row["value_share"],
            },
        )


def load_csv_product_ingredients():
    df = pd.read_csv(csv_product_ingredients)

    for index, row in df.iterrows():
        product = Product.objects.get(product_id=s(row["product_id"]))
        ingredient = Ingredient.objects.get(ingredient_id=s(row["ingredient_id"]))

        prod_ing_uuid = u5(product.product_uuid + ingredient.ingredient_uuid)

        ProductIngredient.objects.update_or_create(
            prod_ing_uuid=prod_ing_uuid,
            defaults={
                "product_uuid": product.product_uuid,
                "ingredient_uuid": ingredient.ingredient_uuid,
                "proportion": row["proportion"],
                "origin_country": s(row.get("origin_country")),
            },
        )


def load_csv_evidence():
    df = pd.read_csv(csv_evidence)

    for index, row in df.iterrows():
        evidence_uuid = u5(s(row["evidence_id"]) + s(row["issuer"]))

        product_uuid = Product.objects.get(product_id=s(row["product_id"])).product_uuid
        stage_uuid = Stage.objects.get(stage_id=s(row["stage_id"])).stage_uuid

        Evidence.objects.update_or_create(
            evidence_uuid=evidence_uuid,
            defaults={
                "evidence_id": s(row["evidence_id"]),
                "scope": s(row["scope"]),
                "type": s(row.get("evidence_type")),
                "issuer": s(row["issuer"]),
                "date": date.today() if pd.isna(row.get("date")) else row.get("date"),
                "summary": s(row.get("summary")),
                "product_uuid": product_uuid,
                "stage_uuid": stage_uuid,
                "file_reference": "",
                "link_reference": "",
            },
        )


def load_csv_claims():
    df = pd.read_csv(csv_claims)

    for index, row in df.iterrows():
        claim_uuid = u5(s(row["claim_id"]) + s(row["claim_type"]))

        product_uuid = Product.objects.get(product_id=s(row["product_id"])).product_uuid
        stage_uuid = Stage.objects.get(stage_id=s(row["stage_id"])).stage_uuid

        Claim.objects.update_or_create(
            claim_uuid=claim_uuid,
            defaults={
                "claim_id": s(row["claim_id"]),
                "product_uuid": product_uuid,
                "stage_uuid": stage_uuid,
                "claim_type": s(row["claim_type"]),
                "statement": s(row.get("statement")),
                "missing_evidence": s(row.get("missing_evidence")).upper() == "TRUE",
            },
        )


def load_csv_claim_evidence():
    df = pd.read_csv(csv_claim_evidence)

    for index, row in df.iterrows():
        claim_uuid = Claim.objects.get(claim_id=s(row["claim_id"])).claim_uuid
        evidence_uuid = Evidence.objects.get(evidence_id=s(row["evidence_id"])).evidence_uuid

        ClaimEvidence.objects.update_or_create(
            claim_uuid=claim_uuid,
            evidence_uuid=evidence_uuid,
        )


def run():
    load_csv_products()
    load_csv_ingredients()
    load_csv_nodes()
    load_csv_stages()
    load_csv_product_ingredients()
    load_csv_evidence()
    load_csv_claims()
    load_csv_claim_evidence()
