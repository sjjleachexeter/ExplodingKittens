from django.contrib.auth.models import User
from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


"""
sources used:
https://docs.djangoproject.com/en/6.0/intro/tutorial02/
https://docs.djangoproject.com/en/4.2/ref/databases/

uuids were used for better uniqueness instead of increamentation approach
"""

class Product(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    product_id = models.CharField(max_length= 100, unique = True)
    name = models.CharField(max_length = 150)
    category = models.CharField(max_length = 100, db_index=True)
    description = models.TextField(blank=True)
    #index is set to true for fast lokups
    qr_token = models.CharField(max_length = 100, unique = True, db_index = True)
    #could add evidence score cache latr
    #evidence_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} ({self.product_id})"

class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default =uuid.uuid4, editable= False)
    ingredient_id = models.CharField(max_length= 100, unique =True)
    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name

class ProductIngredient(models.Model):
    """
    This table connects products to ingredients, used due to the many to many relationship
    """
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="composition")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, related_name="used_in")
    proportion = models.DecimalField(max_digits = 5, decimal_places =4,validators = [MinValueValidator(0), MaxValueValidator(1)])
    origin_country = models.CharField(max_length = 2) # 2 letter country code

class NodeRole(models.TextChoices):
    """
    used enum type for the type of nodes
    """
    FARM = "farm","Farm"
    FACTORY = "factory", "Factory"
    REFINERY = "refinery","Refinery"
    RETAILER= "retailer","Retailer"
    ASSEMBLER = "assembler", "Assembler"
    DISTRIBUTOR = "distributor", "Distributor"
    OTHER = "other", "Other"

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    node_id = models.CharField(max_length = 100, unique=True)
    org_name = models.CharField(max_length = 160)
    role = models.CharField(max_length = 20, choices=NodeRole.choices, default=NodeRole.OTHER)
    country = models.CharField(max_length = 2) #using 2 letter country codes
    city = models.CharField(max_length = 100, blank=True)

    def __str__(self):
        return f"{self.org_name} ({self.country})"

class Stage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stage_id = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= "stages")

    sequence = models.PositiveIntegerField()
    stage_name = models.CharField(max_length = 150)

    from_node = models.ForeignKey(Node, on_delete = models.PROTECT, related_name ="stages_out")
    to_node = models.ForeignKey(Node, on_delete = models.PROTECT, related_name= "stages_in")

    value_share = models.DecimalField(max_digits=5, decimal_places=2, validators = [MinValueValidator(0), MaxValueValidator(100)])

    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)


class EvidenceScope(models.TextChoices):
    PRODUCT = "product", "Product"
    STAGE = "stage", "Stage"

class Evidence(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    evidence_id = models.CharField(max_length = 100, unique = True)

    scope = models.CharField(max_length = 20, choices = EvidenceScope.choices)
    evidence_type = models.CharField(max_length = 50)

    issuer = models.CharField(max_length = 200)
    date = models.DateField()
    summary = models.TextField()

    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True, blank = True, related_name = "evidence_items")
    stage = models.ForeignKey(Stage, on_delete = models.CASCADE, null=True, blank = True, related_name = "evidence_items")

    #links to evidence locally, commented for now
    #file = models.FileField(null=True, blank = True)
    #link_reference = models.URLField(blank=True)

class ClaimType(models.TextChoices):
    ORGANIC ="organic", "Organic"
    LOCAL = "locally_sourced", "Locally sourced"
    FAIRTRADE = "fairtrade", "Fairtrade"
    RECYCLE = "recycled", "Recycled materials"
    OTHER = "other", "Other"

class Claim(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    claim_id = models.CharField(max_length = 100, unique=True)

    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "claims")
    stage = models.ForeignKey(Stage, on_delete = models.SET_NULL, null = True, blank=True, related_name = "claims")

    claim_type = models.CharField(max_length = 50, choices = ClaimType.choices, default =ClaimType.OTHER)
    statement = models.CharField(max_length = 300)

    missing_evidence = models.BooleanField(default = False)

class ClaimEvidence(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable =False)
    claim = models.ForeignKey(Claim, on_delete= models.CASCADE, related_name = "claim_evidence_links")
    evidence = models.ForeignKey(Evidence, on_delete =models.CASCADE, related_name = "claim_evidence_links")

class ProductScan(models.Model):
    id =models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    product= models.ForeignKey(Product, on_delete = models.CASCADE, related_name="scans")
    #has to be connected to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "scans")
    source = models.CharField(max_length = 20, default = "qr")




