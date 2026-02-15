import pandas
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
csv_products = "passport/initialData/products.csv"
csv_ingredients = "passport/initialData/ingredients.csv"
csv_product_ingredients = "passport/initialData/product_ingredients.csv"
csv_nodes = "passport/initialData/nodes.csv"
csv_stages = "passport/initialData/stages.csv"
csv_evidence = "passport/initialData/evidence.csv"
csv_claims = "passport/initialData/claims.csv"
csv_claim_evidence = "passport/initialData/claim_evidence.csv"

# UUIDv5 helpers
NAMESPACE = uuid.NAMESPACE_URL


def u5(text: str) -> str:
    return str(uuid.uuid5(NAMESPACE, text))


def s(v) -> str:
    return "" if pd.isna(v) else str(v).strip()


def load_csv_products():
    df = pd.read_csv(csv_products)
    for index, row in df.iterrows():

        Product.objects.update_or_create(
            id=row["product_uuid"],
            defaults={
                "product_id": int(float(row["product_id"])),
                "name": s(row["name"]),
                "category": s(row["category"]),
                "description": s(row.get("description")),
                "qr_token": int(float(row["product_id"])),
            },
        )


def load_csv_ingredients():
    df = pd.read_csv(csv_ingredients)

    for index, row in df.iterrows():
        Ingredient.objects.update_or_create(
            id=row["ingredient_uuid"],
            defaults={
                "ingredient_id": s(row["ingredient_id"]),
                "name": s(row["name"]),
            },
        )


def load_csv_nodes():
    df = pd.read_csv(csv_nodes)

    for index, row in df.iterrows():
        Node.objects.update_or_create(
            id=row["node_uuid"],
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

        try:
            product = Product.objects.get(id=(row["product_uuid"]))
            from_node_uuid = Node.objects.get(id=(row["from_node"]))
            to_node_uuid = Node.objects.get(id=(row["to_node"]))

            stage_uuid = u5(s(row["stage_id"]) + s(row["sequence"]) + s(row["stage_name"]))

            Stage.objects.update_or_create(
                id=stage_uuid,
                defaults={
                    "stage_id": s(row["stage_id"]),
                    "product": product,
                    "sequence": int(row["sequence"]),
                    "stage_name": s(row["stage_name"]),
                    "from_node": from_node_uuid,
                    "to_node": to_node_uuid,
                    "value_share": row["value_share"],
                },
            )
        except Product.DoesNotExist:
            print(f"could not find product uuid:{row["product_uuid"]}")
        except Node.DoesNotExist:
            print(f"could not find node uuid:{row["from_node"]} or {row["to_node"]}")


def load_csv_product_ingredients():
    df = pd.read_csv(csv_product_ingredients)

    for index, row in df.iterrows():
        try:
            product = Product.objects.get(id=s(row["product_uuid"]))
            ingredient = Ingredient.objects.get(id=s(row["ingredient_uuid"]))
            ProductIngredient.objects.update_or_create(
                id=s(row["prod_ing_uuid"]),
                defaults={
                    "product": product,
                    "ingredient": ingredient,
                    "proportion": row["proportion"],
                    "origin_country": s(row.get("origin_country")),
                },
            )
        except Product.DoesNotExist:
            print(f"could not find product uuid:{row["product_uuid"]}")


def load_csv_evidence():
    df = pd.read_csv(csv_evidence)

    for index, row in df.iterrows():
        evidence_uuid = u5(s(row["evidence_id"]) + s(row["issuer"]))

        product = Product.objects.get(id=s(row["product_uuid"]))

        if not pandas.notnull(row["stage_uuid"]):
            stage = None
        else:
            stage = Stage.objects.get(id=s(row["stage_uuid"]))
        Evidence.objects.update_or_create(
            id=evidence_uuid,
            defaults={
                "evidence_id": s(row["evidence_id"]),
                "scope": s(row["scope"]),
                "evidence_type": s(row.get("evidence_type")),
                "issuer": s(row["issuer"]),
                "date": date.today() if pd.isna(row.get("date")) or row["date"] == "unknown" else pd.to_datetime(
                    row.get("date")),
                "summary": s(row.get("summary")),
                "product": product,
                "stage": stage,

            },
        )


def load_csv_claims():
    df = pd.read_csv(csv_claims)

    for index, row in df.iterrows():

        try:
            product = Product.objects.get(id=s(row["product_uuid"]))
            if not pandas.notnull(row["stage_uuid"]):
                stage = None
            else:
                stage = Stage.objects.get(id=s(row["stage_uuid"]))

            Claim.objects.update_or_create(
                id=row["claim_uuid"],
                defaults={
                    "claim_id": s(row["claim_id"]),
                    "product": product,
                    "stage": stage,
                    "claim_type": s(row["claim_type"]),
                    "statement": s(row.get("statement")),
                    "missing_evidence": s(row.get("missing_evidence")).upper() == "TRUE",
                },
            )
        except Product.DoesNotExist:
            print(f"could not find product uuid:{row["product_uuid"]}")
        except Stage.DoesNotExist:
            print(f"could not find stage uuid:{row["stage_uuid"]}")


def load_csv_claim_evidence():
    df = pd.read_csv(csv_claim_evidence)

    for index, row in df.iterrows():
        try:
            claim = Claim.objects.get(id=s(row["claim_uuid"]))
            evidence = Evidence.objects.get(id=s(row["evidence_uuid"]))

            ClaimEvidence.objects.update_or_create(
                claim=claim,
                evidence=evidence,
            )
        except ClaimEvidence.DoesNotExist:
            print(f"could not find claim uuid:{row["claim_uuid"]}")
        except Evidence.DoesNotExist:
            print(f"could not find evidence uuid:{row["evidence_uuid"]}")


def run():
    load_csv_products()
    load_csv_ingredients()
    load_csv_nodes()
    load_csv_stages()
    load_csv_product_ingredients()
    load_csv_evidence()
    load_csv_claims()
    load_csv_claim_evidence()
