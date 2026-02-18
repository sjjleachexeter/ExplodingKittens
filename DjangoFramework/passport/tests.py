from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.contrib.auth.models import User
from decimal import Decimal

from datetime import datetime

from .models import Product, Ingredient, ProductIngredient, Stage, Ingredient, Node, NodeRole, EvidenceScope, ClaimType, Stage, Evidence, Claim, ClaimEvidence, ProductScan

# Create your tests here.

#Views
class TestDisplayPassport(TestCase):
    def setUp(self):
        self.client = Client()
        self.missing_display_passport_url = reverse('passport_display', args=[123456789])

        self.product = Product.objects.create(
            id = 1,
            product_id = '987654321',
            name = 'Test Product',
            category = 'Test Category',
            description = 'Test Description',
            qr_token = 'Test qr token'
        )

        self.ingredient = Ingredient.objects.create(
            id=1,
            ingredient_id='test ingredent',
            name='test ingredient'
        )
        
        self.product_ingredient = ProductIngredient.objects.create(
            id=1,
            product=self.product,
            ingredient=self.ingredient,
            proportion=1,
            origin_country='GB'
        )

        self.node1 = Node.objects.create(
            id=1,
            node_id='1',
            org_name='test node',
            country='GB',
            city='London'
        )

        self.node2 = Node.objects.create(
            id=2,
            node_id='2',
            org_name='test node 2',
            country='GB',
            city='London'
        )

        self.stage = Stage.objects.create(
            id=1,
            stage_id='test stage',
            product=self.product,
            
            sequence=1,
            stage_name='test stage',

            from_node=self.node1,
            to_node=self.node2,

            value_share=50,
        )

        self.display_passport_url = reverse('passport_display', args=[987654321])

    def test_display_passport(self):
        response = self.client.get(self.display_passport_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "passport/passport.html")

    def test_display_passport_missing(self):
        response = self.client.get(self.missing_display_passport_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "passport/passportNotExisting.html")

class TestReturnToScanner(TestCase):
    def setUp(self):
        self.client = Client()
        self.return_to_scanner_url = reverse('passport_return_to_scanner')

    def test_return_to_scanner(self):
        response = self.client.get(self.return_to_scanner_url)

        self.assertEqual(response.status_code, 302)

#Models
class TestProduct(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            id = 1,
            product_id = 'test Product id',
            name = 'Test Product',
            category = 'Test Category',
            description = 'Test Description',
            qr_token = 'Test qr token'
        )

    def test_product_create(self):
        self.assertTrue(Product.objects.filter(id=1).exists())

    def test_product_read_id(self):
        self.assertEqual(self.product.id, 1)

    def test_product_read_product_id(self):
        self.assertEqual(self.product.product_id, 'test Product id')

    def test_product_read_name(self):
        self.assertEqual(self.product.name, 'Test Product')

    def test_product_read_category(self):
        self.assertEqual(self.product.category, 'Test Category')
    
    def test_product_read_description(self):
        self.assertEqual(self.product.description, 'Test Description')

    def test_product_read_qr_token(self):
        self.assertEqual(self.product.qr_token, 'Test qr token')

    def test_product_update_id(self):
        self.product.id = 2

        self.assertTrue(Product.objects.filter(id=1).exists()) 
        self.assertFalse(Product.objects.filter(id=2).exists())
    
    def test_product_unique_id(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                product2 = Product.objects.create(
                    id = 1,
                    product_id = 'test Product id 2',
                    name = 'Test Product 2',
                    category = 'Test Category 2',
                    description = 'Test Description 2',
                    qr_token = 'Test qr token 2'
                )

        self.assertEqual(Product.objects.filter(id=1).count(), 1)

    def test_product_unique_product_id(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                product2 = Product.objects.create(
                    id = 2,
                    product_id = 'test Product id',
                    name = 'Test Product 2',
                    category = 'Test Category 2',
                    description = 'Test Description 2',
                    qr_token = 'Test qr token 2'
                )

        self.assertEqual(Product.objects.filter(product_id='test Product id').count(), 1)

    def test_product_unique_qr_code(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                product2 = Product.objects.create(
                    id = 2,
                    product_id = 'test Product id 2',
                    name = 'Test Product 2',
                    category = 'Test Category 2',
                    description = 'Test Description 2',
                    qr_token = 'Test qr token'
                )

        self.assertEqual(Product.objects.filter(qr_token='Test qr token').count(), 1)

    def test_product_update_product_id(self):
        self.product.product_id = 'update test'

        self.assertEqual(self.product.product_id, 'update test')

    def test_product_product_id_length_1(self):
        id = 'a' * 99
        self.product.product_id = id
        self.product.full_clean()

        self.assertEqual(self.product.product_id, id)

    def test_product_product_id_length_2(self):
        id = 'a' * 100
        self.product.product_id = id
        self.product.full_clean()

        self.assertEqual(self.product.product_id, id)

    def test_product_product_id_length_3(self):
        id = 'a' * 101
        self.product.product_id = id

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_product_id_length_4(self):
        id = 'a' * 200
        self.product.product_id = id

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_update_name(self):
        self.product.name = 'update test'

        self.assertEqual(self.product.name, 'update test')

    def test_product_name_length_1(self):
        name = 'a' * 149
        self.product.name = name
        self.product.full_clean()

        self.assertEqual(self.product.name, name)
    
    def test_product_name_length_2(self):
        name = 'a' * 150
        self.product.name = name
        self.product.full_clean()

        self.assertEqual(self.product.name, name)
    
    def test_product_name_length_3(self):
        name = 'a' * 151
        self.product.name = name

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_name_length_4(self):
        name = 'a' * 200
        self.product.name = name

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_update_category(self):
        self.product.category = 'update test'

        self.assertEqual(self.product.category, 'update test')

    def test_product_category_length_1(self):
        category = 'a' * 99
        self.product.category = category
        self.product.full_clean()

        self.assertEqual(self.product.category, category)

    def test_product_category_length_2(self):
        category = 'a' * 100
        self.product.category = category
        self.product.full_clean()

        self.assertEqual(self.product.category, category)

    def test_product_category_length_3(self):
        category = 'a' * 101
        self.product.category = category

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_category_length_4(self):
        category = 'a' * 200
        self.product.category = category

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_update_description(self):
        self.product.description = 'update test'

        self.assertEqual(self.product.description, 'update test')

    def test_product_update_qr_token(self):
        self.product.qr_token = 'update test'

        self.assertEqual(self.product.qr_token, 'update test')

    def test_product_qr_token_length_1(self):
        qr_token = 'a' * 99
        self.product.qr_token = qr_token
        self.product.full_clean()

        self.assertEqual(self.product.qr_token, qr_token)

    def test_product_qr_token_length_2(self):
        qr_token = 'a' * 100
        self.product.qr_token = qr_token
        self.product.full_clean()

        self.assertEqual(self.product.qr_token, qr_token)

    def test_product_qr_token_length_3(self):
        qr_token = 'a' * 101
        self.product.qr_token = qr_token

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_qr_token_length_4(self):
        qr_token = 'a' * 200
        self.product.qr_token = qr_token

        with self.assertRaises(ValidationError):
            self.product.full_clean()

    def test_product_delete(self):
        self.product.delete()

        self.assertFalse(Product.objects.filter(id=1).exists())

    def test_product_missing_id(self):
        product2 = Product.objects.create(
            product_id = 'test Product id 2',
            name = 'Test Product 2',
            category = 'Test Category 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )
        self.product.full_clean()
        
        self.assertTrue(Product.objects.filter(id=product2.id).exists())

    def test_product_missing_product_id(self):
        product2 = Product.objects.create(
            id=2,
            name = 'Test Product 2',
            category = 'Test Category 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )

        with self.assertRaises(ValidationError):
            product2.full_clean()

    def test_product_missing_name(self):
        product2 = Product.objects.create(
            id=2,
            product_id = 'test Product id 2',
            category = 'Test Category 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )

        with self.assertRaises(ValidationError):
            product2.full_clean()
        
    def test_product_missing_category(self):
        product2 = Product.objects.create(
            id=2,
            product_id = 'test Product id 2',
            name = 'Test Product 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )

        with self.assertRaises(ValidationError):
            product2.full_clean()
        
    def test_product_missing_description(self):
        product2 = Product.objects.create(
            id=2,
            product_id = 'test Product id 2',
            name = 'Test Product 2',
            category = 'Test Category 2',
            qr_token = 'Test qr token 2'
        )
        self.product.full_clean()
        
        self.assertTrue(Product.objects.filter(id=2).exists())

    def test_product_missing_qr_token(self):
        product2 = Product.objects.create(
            id=2,
            product_id = 'test Product id 2',
            name = 'Test Product 2',
            category = 'Test Category 2',
            description = 'Test Description 2'
        )

        with self.assertRaises(ValidationError):
            product2.full_clean()
        
class TestIngredient(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            id=1,
            ingredient_id='test ingredient',
            name='test ingredient'
        )

    #create
    def test_ingredient_create(self):
        self.assertTrue(Ingredient.objects.filter(id=1).exists())
    
    #read
    def test_ingredient_read_id(self):
        self.assertEqual(self.ingredient.id, 1)

    def test_ingredient_read_ingredient_id(self):
        self.assertEqual(self.ingredient.ingredient_id, 'test ingredient')
    
    def test_ingredient_read_name(self):
        self.assertEqual(self.ingredient.name, 'test ingredient')

    #update
    def test_ingredient_update_id(self):
        self.ingredient.id = 2

        self.assertFalse(Ingredient.objects.filter(id=2).exists())
        self.assertTrue(Ingredient.objects.filter(id=1).exists())

    def test_ingredient_update_ingredient_id(self):
        self.ingredient.ingredient_id = 'new ingredient_id'

        self.assertEqual(self.ingredient.ingredient_id, 'new ingredient_id')
    
    def test_ingredient_update_name(self):
        self.ingredient.name = 'new name'

        self.assertEqual(self.ingredient.name, 'new name')

    #delete
    def test_ingredient_delete_id(self):
        self.ingredient.delete()

        self.assertFalse(Ingredient.objects.filter(id=1).exists())

    #constraints
    def test_ingredient_unique_id(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ingredient2 = Ingredient.objects.create(
                    id=1,
                    ingredient_id='test ingredient 2',
                    name='test ingredient 2'
                )

        self.assertEqual(Ingredient.objects.filter(id=1).count(), 1)

    def test_ingredient_ingredient_id_length_1(self):
        ingredient_id = 'a' * 99
        self.ingredient.ingredient_id = ingredient_id
        self.ingredient.full_clean()

        self.assertEqual(self.ingredient.ingredient_id, ingredient_id)

    def test_ingredient_ingredient_id_length_2(self):
        ingredient_id = 'a' * 100
        self.ingredient.ingredient_id = ingredient_id
        self.ingredient.full_clean()

        self.assertEqual(self.ingredient.ingredient_id, ingredient_id)

    def test_ingredient_ingredient_id_length_3(self):
        ingredient_id = 'a' * 101
        self.ingredient.ingredient_id = ingredient_id

        with self.assertRaises(ValidationError):
            self.ingredient.full_clean()

    def test_ingredient_ingredient_id_length_4(self):
        ingredient_id = 'a' * 150
        self.ingredient.ingredient_id = ingredient_id

        with self.assertRaises(ValidationError):
            self.ingredient.full_clean()

    def test_ingredient_name_length_1(self):
        name = 'a' * 99
        self.ingredient.name = name
        self.ingredient.full_clean()

        self.assertEqual(self.ingredient.name, name)

    def test_ingredient_name_length_2(self):
        name = 'a' * 100
        self.ingredient.name = name
        self.ingredient.full_clean()

        self.assertEqual(self.ingredient.name, name)

    def test_ingredient_name_length_3(self):
        name = 'a' * 101
        self.ingredient.name = name

        with self.assertRaises(ValidationError):
            self.ingredient.full_clean()

    def test_ingredient_name_length_4(self):
        name = 'a' * 150
        self.ingredient.name = name

        with self.assertRaises(ValidationError):
            self.ingredient.full_clean()

class TestProductIngredients(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            id = 1,
            product_id = 'test Product id',
            name = 'Test Product',
            category = 'Test Category',
            description = 'Test Description',
            qr_token = 'Test qr token'
        )

        self.ingredient = Ingredient.objects.create(
            id=1,
            ingredient_id='test ingredient',
            name='test ingredient'
        )

        self.product_ingredient = ProductIngredient.objects.create(
            id=1,
            product=self.product,
            ingredient=self.ingredient,
            proportion=1,
            origin_country='GB'
        )

    #create
    def test_product_ingredients_create(self):
        self.assertTrue(ProductIngredient.objects.filter(id=1).exists())

    #read
    def test_product_ingredients_read_id(self):
        self.assertEqual(self.product_ingredient.id, 1)

    def test_product_ingredients_read_product(self):
        self.assertEqual(self.product_ingredient.product, self.product)

    def test_product_ingredients_read_ingredient(self):
        self.assertEqual(self.product_ingredient.ingredient, self.ingredient)

    def test_product_ingredients_read_proportion(self):
        self.assertEqual(self.product_ingredient.proportion, 1)

    def test_product_ingredients_read_origin_country(self):
        self.assertEqual(self.product_ingredient.origin_country, 'GB')

    #update
    def test_product_ingredients_update_id(self):
        self.product_ingredient.id = 2

        self.assertFalse(ProductIngredient.objects.filter(id=2).exists())
        self.assertTrue(ProductIngredient.objects.filter(id=1).exists())

    def test_product_ingredients_update_product(self):
        product = Product.objects.create(
            id = 2,
            product_id = 'test Product id 2',
            name = 'Test Product 2',
            category = 'Test Category 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )
        self.product_ingredient.product = product

        self.assertEqual(self.product_ingredient.product, product)

    def test_product_ingredients_update_ingredient(self):
        ingredient = Ingredient.objects.create(
            id=2,
            ingredient_id='test ingredient 2',
            name='test ingredient 2'
        )
        self.product_ingredient.ingredient = ingredient

        self.assertEqual(self.product_ingredient.ingredient, ingredient)

    def test_product_ingredients_update_proportion(self):
        self.product_ingredient.proportion = 0.5

        self.assertEqual(self.product_ingredient.proportion, 0.5)

    def test_product_ingredients_update_origin_country(self):
        self.product_ingredient.origin_country = 'US'

        self.assertEqual(self.product_ingredient.origin_country, 'US')

    #delete
    def test_product_ingredients_delete(self):
        self.product_ingredient.delete()

        self.assertFalse(ProductIngredient.objects.filter(id=1).exists())

    def test_product_ingredients_delete_product(self):
        self.product.delete()

        self.assertFalse(ProductIngredient.objects.filter(id=1).exists())

    def test_product_ingredients_delete_ingredient(self):
        with self.assertRaises(ProtectedError):
            self.ingredient.delete()

    #constraints
    def test_product_ingredients_unique_id(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                product_ingredient2 = ProductIngredient.objects.create(
                    id=1,
                    product=self.product,
                    ingredient=self.ingredient,
                    proportion=1,
                    origin_country='GB'
                )

        self.assertEqual(Ingredient.objects.filter(id=1).count(), 1)

    def test_product_ingredients_proportion_max_digits_1(self):
        self.product_ingredient.proportion = 1
        self.product_ingredient.full_clean()

        self.assertEqual(self.product_ingredient.proportion, 1)

    def test_product_ingredients_proportion_max_digits_2(self):
        self.product_ingredient.proportion = Decimal('0.1111')
        self.product_ingredient.full_clean()

        self.assertEqual(self.product_ingredient.proportion, round(Decimal(0.1111),4))

    def test_product_ingredients_proportion_max_digits_3(self):
        self.product_ingredient.proportion = Decimal('0.11111')

        with self.assertRaises(ValidationError):
            self.product_ingredient.full_clean()

    def test_product_ingredients_proportion_max_digits_4(self):
        self.product_ingredient.proportion = Decimal('0.11111111111')

        with self.assertRaises(ValidationError):
            self.product_ingredient.full_clean()

    def test_product_ingredient_proportion_size_8(self):
        self.product_ingredient.proportion = Decimal(0.5)
        
        self.product_ingredient.full_clean()
        self.assertEqual(self.product_ingredient.proportion, round(Decimal(0.5),4))

    def test_product_ingredient_proportion_size_1(self):
        self.product_ingredient.proportion = 1
        
        self.product_ingredient.full_clean()
        self.assertEqual(self.product_ingredient.proportion, 1)

    def test_product_ingredient_proportion_size_2(self):
        self.product_ingredient.proportion = Decimal(1.1)
        
        with self.assertRaises(ValidationError):
            self.product_ingredient.full_clean()

    def test_product_ingredient_proportion_size_3(self):
        self.product_ingredient.proportion = Decimal(1.7)
        
        with self.assertRaises(ValidationError):
            self.product_ingredient.full_clean()

    def test_product_ingredient_proportion_size_4(self):
        self.product_ingredient.proportion = 0
        
        self.product_ingredient.full_clean()
        self.assertEqual(self.product_ingredient.proportion, 0)

    def test_product_ingredient_proportion_size_5(self):
        self.product_ingredient.proportion = round(Decimal(0.1),4)
        
        self.product_ingredient.full_clean()
        self.assertEqual(self.product_ingredient.proportion, round(Decimal(0.1),4))

    def test_product_ingredient_proportion_size_6(self):
        self.product_ingredient.proportion = Decimal(-0.01)
        
        with self.assertRaises(ValidationError):
            self.product_ingredient.full_clean()

    def test_product_ingredient_proportion_size_7(self):
        self.product_ingredient.proportion = Decimal(-1.5)
        
        with self.assertRaises(ValidationError):
            self.product_ingredient.full_clean()

    def test_product_ingredient_origin_country_size_1(self):
        self.product_ingredient.origin_country = 'A'

        with self.assertRaises(ValidationError):
            self.product_ingredient.full_clean()

    def test_product_ingredient_origin_country_size_2(self):
        self.product_ingredient.origin_country = 'AB'
        self.product_ingredient.full_clean()

        self.assertEqual(self.product_ingredient.origin_country, 'AB')

    def test_product_ingredient_origin_country_size_3(self):
        self.product_ingredient.origin_country = 'ABC'

        with self.assertRaises(ValidationError):
            self.product_ingredient.full_clean()

class TestNodeRole(TestCase):
    def test_node_role_farm(self):
        self.assertEqual(NodeRole.FARM.value, 'farm')
        self.assertEqual(NodeRole.FARM.label, 'Farm')

    def test_node_role_factory(self):
        self.assertEqual(NodeRole.FACTORY.value, 'factory')
        self.assertEqual(NodeRole.FACTORY.label, 'Factory')

    def test_node_role_refinery(self):
        self.assertEqual(NodeRole.REFINERY.value, 'refinery')
        self.assertEqual(NodeRole.REFINERY.label, 'Refinery')

    def test_node_role_retailer(self):
        self.assertEqual(NodeRole.RETAILER.value, 'retailer')
        self.assertEqual(NodeRole.RETAILER.label, 'Retailer')

    def test_node_role_assembler(self):
        self.assertEqual(NodeRole.ASSEMBLER.value, 'assembler')
        self.assertEqual(NodeRole.ASSEMBLER.label, 'Assembler')

    def test_node_role_distributer(self):
        self.assertEqual(NodeRole.DISTRIBUTOR.value, 'distributor')
        self.assertEqual(NodeRole.DISTRIBUTOR.label, 'Distributor')

    def test_node_role_other(self):
        self.assertEqual(NodeRole.OTHER.value, 'other')
        self.assertEqual(NodeRole.OTHER.label, 'Other')

class TestNode(TestCase):
    def setUp(self):
        self.node = Node.objects.create(
            id=1,
            node_id='1',
            org_name='test name',
            role=NodeRole.FARM,
            country='GB',
            city='London'
        )

    #create
    def test_node_create(self):
        self.assertTrue(Node.objects.filter(id=1).exists())

    #read
    def test_node_id_read(self):
        self.assertEqual(self.node.id, 1)

    def test_node_node_id_read(self):
        self.assertEqual(self.node.node_id, '1')

    def test_node_org_name_read(self):
        self.assertEqual(self.node.org_name, 'test name')

    def test_node_role_read(self):
        self.assertEqual(self.node.role, NodeRole.FARM)

    def test_node_country_read(self):
        self.assertEqual(self.node.country, 'GB')

    def test_node_city_read(self):
        self.assertEqual(self.node.city, 'London')

    #update
    def test_node_id_update(self):
        self.node.id = 2

        self.assertFalse(Node.objects.filter(id=2).exists())
        self.assertTrue(Node.objects.filter(id=1).exists())

    def test_node_node_id_update(self):
        self.node.id = '2'

        self.assertEqual(self.node.id, '2')
    
    def test_node_org_name_update(self):
        self.node.org_name = 'test name 2'

        self.assertEqual(self.node.org_name, 'test name 2')

    def test_node_role_update(self):
        self.node.role = NodeRole.ASSEMBLER

        self.assertEqual(self.node.role, NodeRole.ASSEMBLER)

    def test_node_country_update(self):
        self.node.country = 'US'

        self.assertEqual(self.node.country, 'US')

    def test_node_city_update(self):
        self.node.city = 'test'

        self.assertEqual(self.node.city, 'test')

    #delete
    def test_node_delete(self):
        self.node.delete()

        self.assertFalse(Node.objects.filter(id=1).exists())

    #constraints
    def test_node_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.node = Node.objects.create(
                    id=1,
                    node_id='2',
                    org_name='test name',
                    role=NodeRole.FARM,
                    country='GB',
                    city='London'
                )
        self.assertEqual(Node.objects.filter(id=1).count(),1)
    
    def test_node_node_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.node = Node.objects.create(
                    id=2,
                    node_id='1',
                    org_name='test name',
                    role=NodeRole.FARM,
                    country='GB',
                    city='London'
                )
        self.assertEqual(Node.objects.filter(node_id='1').count(),1)
    
    def test_node_node_id_length_1(self):
        node_id = '1' * 99
        self.node.node_id = node_id
        self.node.full_clean()

        self.assertEqual(self.node.node_id, node_id)

    def test_node_node_id_length_2(self):
        node_id = '1' * 100
        self.node.node_id = node_id
        self.node.full_clean()

        self.assertEqual(self.node.node_id, node_id)

    def test_node_node_id_length_3(self):
        node_id = '1' * 101
        self.node.node_id = node_id

        with self.assertRaises(ValidationError):
            self.node.full_clean()

    def test_node_node_id_length_4(self):
        node_id = '1' * 150
        self.node.node_id = node_id

        with self.assertRaises(ValidationError):
            self.node.full_clean()

    def test_node_org_name_length_1(self):
        org_name = 'a' * 159
        self.node.org_name = org_name
        self.node.full_clean()
        
        self.assertEqual(self.node.org_name, org_name)

    def test_node_org_name_length_2(self):
        org_name = 'a' * 160
        self.node.org_name = org_name
        self.node.full_clean()
        
        self.assertEqual(self.node.org_name, org_name)

    def test_node_org_name_length_3(self):
        org_name = 'a' * 161
        self.node.org_name = org_name

        with self.assertRaises(ValidationError):
            self.node.full_clean()
        
    def test_node_org_name_length_4(self):
        org_name = 'a' * 200
        self.node.org_name = org_name
        
        with self.assertRaises(ValidationError):
            self.node.full_clean()

    def test_node_country_length_1(self):
        self.node.country = 'A'
        with self.assertRaises(ValidationError):
            self.node.full_clean()

    def test_node_country_length_2(self):
        self.node.country = 'AB'
        self.node.full_clean()

        self.assertEqual(self.node.country, 'AB')

    def test_node_country_length_3(self):
        self.node.country = 'ABC'
        with self.assertRaises(ValidationError):
            self.node.full_clean()

    def test_node_country_length_4(self):
        self.node.country = 'ABCDEFGHIJK'
        with self.assertRaises(ValidationError):
            self.node.full_clean()

    def test_node_city_length_1(self):
        city = 'a' * 99
        self.node.city = city
        self.node.full_clean()

        self.assertEqual(self.node.city, city)

    def test_node_city_length_2(self):
        city = 'a' * 100
        self.node.city = city
        self.node.full_clean()

        self.assertEqual(self.node.city, city)

    def test_node_city_length_3(self):
        city = 'a' * 101
        self.node.city = city

        with self.assertRaises(ValidationError):
            self.node.full_clean()

    def test_node_city_length_4(self):
        city = 'a' * 150
        self.node.city = city
        
        with self.assertRaises(ValidationError):
            self.node.full_clean()

class TestStage(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            id = 1,
            product_id = 'test Product id',
            name = 'Test Product',
            category = 'Test Category',
            description = 'Test Description',
            qr_token = 'Test qr token'
        )

        self.node = Node.objects.create(
            id=1,
            node_id='1',
            org_name='test name',
            role=NodeRole.FARM,
            country='GB',
            city='London'
        )

        self.stage = Stage.objects.create(
            id=1,
            stage_id='1',
            product=self.product,

            sequence=1,
            stage_name='test stage',

            from_node=self.node,
            to_node=self.node,

            value_share=20,

            date_start=datetime(2026,1,10,5,0),
            date_end=datetime(2026,1,20,5,0)
        )

    #create
    def test_stage_create(self):
        self.assertTrue(Stage.objects.filter(id=1).exists())

    #read
    def test_stage_id_read(self):
        self.assertEqual(self.stage.id, 1)

    def test_stage_stage_id_read(self):
        self.assertEqual(self.stage.stage_id, '1')

    def test_stage_product_read(self):
        self.assertEqual(self.stage.product, self.product)

    def test_stage_sequence_read(self):
        self.assertEqual(self.stage.sequence, 1)

    def test_stage_stage_name_read(self):
        self.assertEqual(self.stage.stage_name, 'test stage')

    def test_stage_from_node_read(self):
        self.assertEqual(self.stage.from_node, self.node)

    def test_stage_to_node_read(self):
        self.assertEqual(self.stage.to_node, self.node)

    def test_stage_value_share_read(self):
        self.assertEqual(self.stage.value_share, 20)

    def test_stage_date_start_read(self):
        self.assertEqual(self.stage.date_start, datetime(2026,1,10,5,0))

    def test_stage_date_end_read(self):
        self.assertEqual(self.stage.date_end, datetime(2026,1,20,5,0))

    #update
    def test_stage_id_update(self):
        self.stage.id = 2

        self.assertTrue(Stage.objects.filter(id=1).exists())
        self.assertFalse(Stage.objects.filter(id=2).exists())

    def test_stage_stage_id_update(self):
        self.stage.stage_id = '2'

        self.assertEqual(self.stage.stage_id, '2')

    def test_stage_product_update(self):
        product = Product.objects.create(
            id = 2,
            product_id = 'test Product id 2',
            name = 'Test Product 2',
            category = 'Test Category 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )

        self.stage.product = product

        self.assertEqual(self.stage.product, product)

    def test_stage_sequence_update(self):
        self.stage.sequence = 2

        self.assertEqual(self.stage.sequence, 2)

    def test_stage_stage_name_update(self):
        self.stage.stage_name = 'test name 2'

        self.assertEqual(self.stage.stage_name, 'test name 2')

    def test_stage_from_node_update(self):
        node = Node.objects.create(
            id=2,
            node_id='2',
            org_name='test name 2',
            role=NodeRole.FARM,
            country='GB',
            city='London'
        )

        self.stage.from_node = node

        self.assertEqual(self.stage.from_node, node)

    def test_stage_to_node_update(self):
        node = Node.objects.create(
            id=2,
            node_id='2',
            org_name='test name 2',
            role=NodeRole.FARM,
            country='GB',
            city='London'
        )

        self.stage.to_node = node

        self.assertEqual(self.stage.to_node, node)

    def test_stage_value_share_update(self):
        self.stage.value_share = 30

        self.assertEqual(self.stage.value_share, 30)

    def test_stage_date_start_update(self):
        self.stage.date_start = datetime(2026,1,15,5,0)

        self.assertEqual(self.stage.date_start, datetime(2026,1,15,5,0))

    def test_stage_date_end_update(self):
        self.stage.date_end = datetime(2026,1,15,5,0)

        self.assertEqual(self.stage.date_end, datetime(2026,1,15,5,0))

    #delete
    def test_stage_delete(self):
        self.stage.delete()

        self.assertFalse(Stage.objects.filter(id=1).exists())

    def test_stage_delete_product(self):
        self.product.delete()

        self.assertFalse(Stage.objects.filter(id=1).exists())

    def test_stage_delete_node(self):
        with self.assertRaises(ProtectedError):
            self.node.delete()

    #constraints
    def test_stage_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                stage = Stage.objects.create(
                    id=1,
                    stage_id='2',
                    product=self.product,

                    sequence=1,
                    stage_name='test stage 2',

                    from_node=self.node,
                    to_node=self.node,

                    value_share=20,

                    date_start=datetime(2026,1,10,5,0),
                    date_end=datetime(2026,1,20,5,0)
                )

    def test_stage_stage_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                stage = Stage.objects.create(
                    id=2,
                    stage_id='1',
                    product=self.product,

                    sequence=1,
                    stage_name='test stage 2',

                    from_node=self.node,
                    to_node=self.node,

                    value_share=20,

                    date_start=datetime(2026,1,10,5,0),
                    date_end=datetime(2026,1,20,5,0)
                )
    
    def test_stage_stage_id_length_1(self):
        stage_id = '1' * 99
        self.stage.stage_id = stage_id
        self.stage.full_clean()

        self.assertEqual(self.stage.stage_id, stage_id)

    def test_stage_stage_id_length_2(self):
        stage_id = '1' * 100
        self.stage.stage_id = stage_id
        self.stage.full_clean()

        self.assertEqual(self.stage.stage_id, stage_id)

    def test_stage_stage_id_length_3(self):
        stage_id = '1' * 101
        self.stage.stage_id = stage_id

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_stage_id_length_4(self):
        stage_id = '1' * 150
        self.stage.stage_id = stage_id

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_sequence_positive(self):
        self.stage.sequence = -1

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_stage_name_length_1(self):
        stage_name = 'a' * 149
        self.stage.stage_name = stage_name
        self.stage.full_clean()

        self.assertEqual(self.stage.stage_name, stage_name)

    def test_stage_stage_name_length_2(self):
        stage_name = 'a' * 150
        self.stage.stage_name = stage_name
        self.stage.full_clean()

        self.assertEqual(self.stage.stage_name, stage_name)

    def test_stage_stage_name_length_3(self):
        stage_name = 'a' * 151
        self.stage.stage_name = stage_name

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_stage_name_length_4(self):
        stage_name = 'a' * 200
        self.stage.stage_name = stage_name

        with self.assertRaises(ValidationError):
            self.stage.full_clean()
    
    def test_stage_value_share_size_1(self):
        self.stage.value_share = -50

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_value_share_size_2(self):
        self.stage.value_share = -1

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_value_share_size_3(self):
        self.stage.value_share = 0
        self.stage.full_clean()

        self.assertEqual(self.stage.value_share, 0)

    def test_stage_value_share_size_4(self):
        self.stage.value_share = 1
        self.stage.full_clean()

        self.assertEqual(self.stage.value_share, 1)

    def test_stage_value_share_size_5(self):
        self.stage.value_share = 50
        self.stage.full_clean()

        self.assertEqual(self.stage.value_share, 50)

    def test_stage_value_share_size_6(self):
        self.stage.value_share = 99
        self.stage.full_clean()

        self.assertEqual(self.stage.value_share, 99)

    def test_stage_value_share_size_7(self):
        self.stage.value_share = 100
        self.stage.full_clean()

        self.assertEqual(self.stage.value_share, 100)

    def test_stage_value_share_size_8(self):
        self.stage.value_share = 101

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_value_share_size_9(self):
        self.stage.value_share = 150

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_value_share_max_digits_1(self):
        self.stage.value_share = round(Decimal(1.12),2)
        self.stage.full_clean()

        self.assertEqual(self.stage.value_share, round(Decimal(1.12),2))

    def test_stage_value_share_max_digits_2(self):
        self.stage.value_share = round(Decimal(100.00),2)
        self.stage.full_clean()

        self.assertEqual(self.stage.value_share, round(Decimal(100.00),2))

    def test_stage_value_share_max_digits_3(self):
        self.stage.value_share = round(Decimal(1231.12),2)

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_value_share_max_digits_4(self):
        self.stage.value_share = round(Decimal(1234567891.12),2)

        with self.assertRaises(ValidationError):
            self.stage.full_clean()
    
    def test_stage_value_share_decimals_1(self):
        self.stage.value_share = round(Decimal(0.54),2)
        self.stage.full_clean()

        self.assertEqual(self.stage.value_share, round(Decimal(0.54),2))

    def test_stage_value_share_decimals_2(self):
        self.stage.value_share = round(Decimal(0.544),3)

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

    def test_stage_value_share_decimals_3(self):
        self.stage.value_share = round(Decimal(0.544444),6)

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

class TestEvidenceScope(TestCase):
    def test_evidence_scope_product(self):
        self.assertEqual(EvidenceScope.PRODUCT.value, 'product')
        self.assertEqual(EvidenceScope.PRODUCT.label, 'Product')

    def test_evidence_scope_stage(self):
        self.assertEqual(EvidenceScope.STAGE.value, 'stage')
        self.assertEqual(EvidenceScope.STAGE.label, 'Stage')

class TestEvidence(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            id = 1,
            product_id = 'test Product id',
            name = 'Test Product',
            category = 'Test Category',
            description = 'Test Description',
            qr_token = 'Test qr token'
        )

        self.node = Node.objects.create(
            id=1,
            node_id='1',
            org_name='test name',
            role=NodeRole.FARM,
            country='GB',
            city='London'
        )

        self.stage = Stage.objects.create(
            id=1,
            stage_id='1',
            product=self.product,

            sequence=1,
            stage_name='test stage',

            from_node=self.node,
            to_node=self.node,

            value_share=20,

            date_start=datetime(2026,1,10,5,0),
            date_end=datetime(2026,1,20,5,0)
        )

        self.evidence = Evidence.objects.create(
            id=1,
            evidence_id='1',

            scope=EvidenceScope.PRODUCT,
            evidence_type='test evidence',

            issuer='test evidence',
            date=datetime(2026,1,20,5,0),
            summary='test evidence',

            product=self.product,
            stage=self.stage
        )

    #create
    def test_evidence_create(self):
        self.assertTrue(Evidence.objects.filter(id=1).exists())

    #read
    def test_evidence_id_read(self):
        self.assertEqual(self.evidence.id, 1)

    def test_evidence_evidence_id_read(self):
        self.assertEqual(self.evidence.evidence_id, '1')

    def test_evidence_scope_read(self):
        self.assertEqual(self.evidence.scope, EvidenceScope.PRODUCT)

    def test_evidence_evidence_type_read(self):
        self.assertEqual(self.evidence.evidence_type, 'test evidence')

    def test_evidence_issuer_read(self):
        self.assertEqual(self.evidence.issuer, 'test evidence')

    def test_evidence_date_read(self):
        self.assertEqual(self.evidence.date, datetime(2026,1,20,5,0))

    def test_evidence_summary_read(self):
        self.assertEqual(self.evidence.summary, 'test evidence')

    def test_evidence_product_read(self):
        self.assertEqual(self.evidence.product, self.product)

    def test_evidence_stage_read(self):
        self.assertEqual(self.evidence.stage, self.stage)

    #update
    def test_evidence_id_update(self):
        self.evidence.id = 2

        self.assertFalse(Evidence.objects.filter(id=2).exists())
        self.assertTrue(Evidence.objects.filter(id=1).exists())

    def test_evidence_evidence_id_update(self):
        self.evidence.evidence_id = '2'

        self.assertEqual(self.evidence.evidence_id, '2')

    def test_evidence_scope_update(self):
        self.evidence.scope = EvidenceScope.STAGE

        self.assertEqual(self.evidence.scope, EvidenceScope.STAGE)

    def test_evidence_evidence_type_update(self):
        self.evidence.evidence_type = 'new type'

        self.assertEqual(self.evidence.evidence_type, 'new type')

    def test_evidence_issuer_update(self):
        self.evidence.issuer = 'new issuer'

        self.assertEqual(self.evidence.issuer, 'new issuer')

    def test_evidence_date_update(self):
        self.evidence.date = datetime(2026,1,11,5,0)

        self.assertEqual(self.evidence.date, datetime(2026,1,11,5,0))

    def test_evidence_summary_update(self):
        self.evidence.summary = 'new summary'

        self.assertEqual(self.evidence.summary, 'new summary')

    def test_evidence_product_update(self):
        product = Product.objects.create(
            id = 2,
            product_id = 'test Product id 2',
            name = 'Test Product 2',
            category = 'Test Category 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )

        self.evidence.product = product

        self.assertEqual(self.evidence.product, product)

    def test_evidence_stage_update(self):
        stage = Stage.objects.create(
            id=2,
            stage_id='2',
            product=self.product,

            sequence=1,
            stage_name='test stage 2',

            from_node=self.node,
            to_node=self.node,

            value_share=20,

            date_start=datetime(2026,1,10,5,0),
            date_end=datetime(2026,1,20,5,0)
        )

        self.evidence.stage = stage

        self.assertEqual(self.evidence.stage, stage)

    #delete
    def test_evidence_delete(self):
        self.evidence.delete()

        self.assertFalse(Evidence.objects.filter(id=1).exists())

    def test_evidence_product_delete(self):
        self.product.delete()

        self.assertFalse(Evidence.objects.filter(id=1).exists())

    def test_evidence_stage_delete(self):
        self.stage.delete()

        self.assertFalse(Evidence.objects.filter(id=1).exists())

    #constraints
    def test_evidence_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.evidence = Evidence.objects.create(
                    id=1,
                    evidence_id='2',

                    scope=EvidenceScope.PRODUCT,
                    evidence_type='test evidence 2',

                    issuer='test evidence 2',
                    date=datetime(2026,1,20,5,0),
                    summary='test evidence 2',

                    product=self.product,
                    stage=self.stage
                )

    def test_evidence_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.evidence = Evidence.objects.create(
                    id=2,
                    evidence_id='1',

                    scope=EvidenceScope.PRODUCT,
                    evidence_type='test evidence 2',

                    issuer='test evidence 2',
                    date=datetime(2026,1,20,5,0),
                    summary='test evidence 2',

                    product=self.product,
                    stage=self.stage
                )

    def test_evidence_evidence_id_length_1(self):
        evidence_id = '1' * 99
        self.evidence.evidence_id = evidence_id
        self.evidence.full_clean()

        self.assertEqual(self.evidence.evidence_id, evidence_id)

    def test_evidence_evidence_id_length_2(self):
        evidence_id = '1' * 100
        self.evidence.evidence_id = evidence_id
        self.evidence.full_clean()

        self.assertEqual(self.evidence.evidence_id, evidence_id)

    def test_evidence_evidence_id_length_3(self):
        evidence_id = '1' * 101
        self.evidence.evidence_id = evidence_id

        with self.assertRaises(ValidationError):
            self.evidence.full_clean()

    def test_evidence_evidence_id_length_4(self):
        evidence_id = '1' * 150
        self.evidence.evidence_id = evidence_id

        with self.assertRaises(ValidationError):
            self.evidence.full_clean()

    def test_evidence_issuer_length_1(self):
        issuer = 'a' * 199
        self.evidence.issuer = issuer
        self.evidence.full_clean()

        self.assertEqual(self.evidence.issuer, issuer)

    def test_evidence_issuer_length_2(self):
        issuer = 'a' * 200
        self.evidence.issuer = issuer
        self.evidence.full_clean()

        self.assertEqual(self.evidence.issuer, issuer)

    def test_evidence_issuer_length_3(self):
        issuer = 'a' * 201
        self.evidence.issuer = issuer

        with self.assertRaises(ValidationError):
            self.evidence.full_clean()

    def test_evidence_issuer_length_4(self):
        issuer = 'a' * 250
        self.evidence.issuer = issuer

        with self.assertRaises(ValidationError):
            self.evidence.full_clean()

class TestClaimType(TestCase):
    def test_claim_type_organic(self):
        self.assertEqual(ClaimType.ORGANIC.value, 'organic')
        self.assertEqual(ClaimType.ORGANIC.label, 'Organic')

    def test_claim_type_local(self):
        self.assertEqual(ClaimType.LOCAL.value, 'locally_sourced')
        self.assertEqual(ClaimType.LOCAL.label, 'Locally sourced')

    def test_claim_type_fairtrade(self):
        self.assertEqual(ClaimType.FAIRTRADE.value, 'fairtrade')
        self.assertEqual(ClaimType.FAIRTRADE.label, 'Fairtrade')

    def test_claim_type_recycle(self):
        self.assertEqual(ClaimType.RECYCLE.value, 'recycled')
        self.assertEqual(ClaimType.RECYCLE.label, 'Recycled materials')

    def test_claim_type_other(self):
        self.assertEqual(ClaimType.OTHER.value, 'other')
        self.assertEqual(ClaimType.OTHER.label, 'Other')

class TestClaim(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            id = 1,
            product_id = 'test Product id',
            name = 'Test Product',
            category = 'Test Category',
            description = 'Test Description',
            qr_token = 'Test qr token'
        )

        self.node = Node.objects.create(
            id=1,
            node_id='1',
            org_name='test name',
            role=NodeRole.FARM,
            country='GB',
            city='London'
        )

        self.stage = Stage.objects.create(
            id=1,
            stage_id='1',
            product=self.product,

            sequence=1,
            stage_name='test stage',

            from_node=self.node,
            to_node=self.node,

            value_share=20,

            date_start=datetime(2026,1,10,5,0),
            date_end=datetime(2026,1,20,5,0)
        )

        self.claim = Claim.objects.create(
            id=1,
            claim_id='1',
            
            product=self.product,
            stage=self.stage,

            claim_type=ClaimType.FAIRTRADE,
            statement='test claim',

            missing_evidence=False
        )

    #create
    def test_claim_create(self):
        self.assertTrue(Claim.objects.filter(id=1).exists())

    #read
    def test_claim_id_read(self):
        self.assertEqual(self.claim.id, 1)

    def test_claim_claim_id_read(self):
        self.assertEqual(self.claim.claim_id, '1')

    def test_claim_product_read(self):
        self.assertEqual(self.claim.product, self.product)

    def test_claim_stage_read(self):
        self.assertEqual(self.claim.stage, self.stage)

    def test_claim_claim_type_read(self):
        self.assertEqual(self.claim.claim_type, ClaimType.FAIRTRADE)

    def test_claim_statment_read(self):
        self.assertEqual(self.claim.statement, 'test claim')

    def test_claim_missing_evidence_read(self):
        self.assertEqual(self.claim.missing_evidence, False)

    #update
    def test_claim_id_update(self):
        self.claim.id = 2

        self.assertTrue(Claim.objects.filter(id=1).exists())
        self.assertFalse(Claim.objects.filter(id=2).exists())

    def test_claim_claim_id_update(self):
        self.claim.claim_id = '2'

        self.assertEqual(self.claim.claim_id, '2')

    def test_claim_product_update(self):
        product = Product.objects.create(
            id = 2,
            product_id = 'test Product id 2',
            name = 'Test Product 2',
            category = 'Test Category 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )
        self.claim.product = product

        self.assertEqual(self.claim.product, product)

    def test_claim_stage_update(self):
        stage = Stage.objects.create(
            id=2,
            stage_id='2',
            product=self.product,

            sequence=1,
            stage_name='test stage 2',

            from_node=self.node,
            to_node=self.node,

            value_share=20,

            date_start=datetime(2026,1,10,5,0),
            date_end=datetime(2026,1,20,5,0)
        )
        self.claim.stage = stage

        self.assertEqual(self.claim.stage, stage)

    def test_claim_claim_type_update(self):
        self.claim.claim_type = ClaimType.LOCAL

        self.assertEqual(self.claim.claim_type, ClaimType.LOCAL)

    def test_claim_statment_update(self):
        self.claim.statement = 'new statement'

        self.assertEqual(self.claim.statement, 'new statement')

    def test_claim_missing_evidence_update(self):
        self.claim.missing_evidence = True

        self.assertEqual(self.claim.missing_evidence, True)

    #delete
    def test_claim_delete(self):
        self.claim.delete()
        
        self.assertFalse(Claim.objects.filter(id=1).exists())

    def test_claim_product_delete(self):
        self.product.delete()
        
        self.assertFalse(Claim.objects.filter(id=1).exists())

    def test_claim_stage_delete(self):
        self.stage.delete()
        self.claim.refresh_from_db()
        
        self.assertIsNone(self.claim.stage)

    #constraints
    def test_claim_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                claim = Claim.objects.create(
                    id=1,
                    claim_id='2',
                    
                    product=self.product,
                    stage=self.stage,

                    claim_type=ClaimType.FAIRTRADE,
                    statement='test claim 2',

                    missing_evidence=False
                )
    def test_claim_claim_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                claim = Claim.objects.create(
                    id=2,
                    claim_id='1',
                    
                    product=self.product,
                    stage=self.stage,

                    claim_type=ClaimType.FAIRTRADE,
                    statement='test claim 2',

                    missing_evidence=False
                )
    
    def test_claim_claim_id_length_1(self):
        claim_id = '1' * 99
        self.claim.claim_id = claim_id
        self.claim.full_clean()

        self.assertEqual(self.claim.claim_id, claim_id)

    def test_claim_claim_id_length_2(self):
        claim_id = '1' * 100
        self.claim.claim_id = claim_id
        self.claim.full_clean()

        self.assertEqual(self.claim.claim_id, claim_id)

    def test_claim_claim_id_length_3(self):
        claim_id = '1' * 101
        self.claim.claim_id = claim_id

        with self.assertRaises(ValidationError):
            self.claim.full_clean()

    def test_claim_claim_id_length_4(self):
        claim_id = '1' * 150
        self.claim.claim_id = claim_id

        with self.assertRaises(ValidationError):
            self.claim.full_clean()

    def test_claim_statment_length_1(self):
        statement = 'a' * 299
        self.claim.statement = statement
        self.claim.full_clean()

        self.assertEqual(self.claim.statement, statement)

    def test_claim_statment_length_2(self):
        statement = 'a' * 300
        self.claim.statement = statement
        self.claim.full_clean()

        self.assertEqual(self.claim.statement, statement)

    def test_claim_statment_length_3(self):
        statement = 'a' * 301
        self.claim.statement = statement

        with self.assertRaises(ValidationError):
            self.claim.full_clean()

    def test_claim_statment_length_4(self):
        statement = 'a' * 350
        self.claim.statement = statement

        with self.assertRaises(ValidationError):
            self.claim.full_clean()

class TestClaimEvidence(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            id = 1,
            product_id = 'test Product id',
            name = 'Test Product',
            category = 'Test Category',
            description = 'Test Description',
            qr_token = 'Test qr token'
        )

        self.node = Node.objects.create(
            id=1,
            node_id='1',
            org_name='test name',
            role=NodeRole.FARM,
            country='GB',
            city='London'
        )

        self.stage = Stage.objects.create(
            id=1,
            stage_id='1',
            product=self.product,

            sequence=1,
            stage_name='test stage',

            from_node=self.node,
            to_node=self.node,

            value_share=20,

            date_start=datetime(2026,1,10,5,0),
            date_end=datetime(2026,1,20,5,0)
        )

        self.claim = Claim.objects.create(
            id=1,
            claim_id='1',
            
            product=self.product,
            stage=self.stage,

            claim_type=ClaimType.FAIRTRADE,
            statement='test claim',

            missing_evidence=False
        )

        self.evidence = Evidence.objects.create(
            id=1,
            evidence_id='1',

            scope=EvidenceScope.PRODUCT,
            evidence_type='test evidence',

            issuer='test evidence',
            date=datetime(2026,1,20,5,0),
            summary='test evidence',

            product=self.product,
            stage=self.stage
        )

        self.claim_evidence = ClaimEvidence.objects.create(
            id=1,
            claim=self.claim,
            evidence=self.evidence
        )

    #create
    def test_claim_evidence_create(self):
        self.assertTrue(ClaimEvidence.objects.filter(id=1).exists())

    #read
    def test_claim_evidence_id_read(self):
        self.assertEqual(self.claim_evidence.id, 1)

    def test_claim_evidence_claim_read(self):
        self.assertEqual(self.claim_evidence.claim, self.claim)

    def test_claim_evidence_evidence_read(self):
        self.assertEqual(self.claim_evidence.evidence, self.evidence)

    #update
    def test_claim_evidence_id_update(self):
        self.claim.id = 2

        self.assertFalse(ClaimEvidence.objects.filter(id=2).exists())
        self.assertTrue(ClaimEvidence.objects.filter(id=1).exists())

    def test_claim_evidence_claim_update(self):
        claim = Claim.objects.create(
            id=2,
            claim_id='2',
            
            product=self.product,
            stage=self.stage,

            claim_type=ClaimType.FAIRTRADE,
            statement='test claim 2',

            missing_evidence=False
        )
        self.claim_evidence.claim = claim

        self.assertEqual(self.claim_evidence.claim, claim)

    def test_claim_evidence_evidence_update(self):
        evidence = Evidence.objects.create(
            id=2,
            evidence_id='2',

            scope=EvidenceScope.PRODUCT,
            evidence_type='test evidence 2',

            issuer='test evidence 2',
            date=datetime(2026,1,20,5,0),
            summary='test evidence 2',

            product=self.product,
            stage=self.stage
        )
        self.claim_evidence.evidence = evidence

        self.assertEqual(self.claim_evidence.evidence, evidence)

    #delete
    def test_claim_evidence_delete(self):
        self.claim_evidence.delete()

        self.assertFalse(ClaimEvidence.objects.filter(id=1).exists())

    def test_claim_evidence_claim_delete(self):
        self.claim.delete()

        self.assertFalse(ClaimEvidence.objects.filter(id=1).exists())

    def test_claim_evidence_evidence_delete(self):
        self.evidence.delete()

        self.assertFalse(ClaimEvidence.objects.filter(id=1).exists())

    #constraints 
    def test_claim_evidence_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                claim_evidence = ClaimEvidence.objects.create(
                    id=1,
                    claim=self.claim,
                    evidence=self.evidence
                )

class TestProductScan(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            id = 1,
            product_id = '987654321',
            name = 'Test Product',
            category = 'Test Category',
            description = 'Test Description',
            qr_token = 'Test qr token'
        )

        self.user = User.objects.create_user(
            username = 'test',
            password = 'Password123!'
        )

        self.product_scan = ProductScan.objects.create(
            id=1,
            product=self.product,
            user=self.user,
            source='test'
        )

    #create
    def test_product_scan_create(self):
        self.assertTrue(ProductScan.objects.filter(id=1).exists())

    #read
    def test_product_scan_id_read(self):
        self.assertEqual(self.product_scan.id, 1)

    def test_product_scan_product_read(self):
        self.assertEqual(self.product_scan.product, self.product)

    def test_product_scan_user_read(self):
        self.assertEqual(self.product_scan.user, self.user)

    def test_product_scan_source_read(self):
        self.assertEqual(self.product_scan.source, 'test')

    #update
    def test_product_scan_id_update(self):
        self.product_scan.id = 2

        self.assertFalse(ProductScan.objects.filter(id=2).exists())
        self.assertTrue(ProductScan.objects.filter(id=1).exists())

    def test_product_scan_product_update(self):
        product = Product.objects.create(
            id = 2,
            product_id = '2',
            name = 'Test Product 2',
            category = 'Test Category 2',
            description = 'Test Description 2',
            qr_token = 'Test qr token 2'
        )
        self.product_scan.product = product

        self.assertEqual(self.product_scan.product, product)

    def test_product_scan_user_update(self):
        user = User.objects.create_user(
            username = 'test 1',
            password = 'Password123!'
        )
        self.product_scan.user = user

        self.assertEqual(self.product_scan.user, user)

    def test_product_scan_source_update(self):
        self.product_scan.source = 'test 2'

        self.assertEqual(self.product_scan.source, 'test 2')

    #delete
    def test_product_scan_delete(self):
        self.product_scan.delete()

        self.assertFalse(ProductScan.objects.filter(id=1).exists())

    def test_product_scan_product_delete(self):
        self.product.delete()

        self.assertFalse(ProductScan.objects.filter(id=1).exists())

    def test_product_scan_user_delete(self):
        self.user.delete()

        self.assertFalse(ProductScan.objects.filter(id=1).exists())

    #constraints 
    def test_product_scan_id_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                product_scan = ProductScan.objects.create(
                    id=1,
                    product=self.product,
                    user=self.user,
                    source='test 2'
                )
    
    def test_product_scan_source_length_1(self):
        source = 'a' * 19
        self.product_scan.source = source
        self.product_scan.full_clean()

        self.assertEqual(self.product_scan.source, source)

    def test_product_scan_source_length_1(self):
        source = 'a' * 20
        self.product_scan.source = source
        self.product_scan.full_clean()

        self.assertEqual(self.product_scan.source, source)

    def test_product_scan_source_length_1(self):
        source = 'a' * 21
        self.product_scan.source = source

        with self.assertRaises(ValidationError):
            self.product_scan.full_clean()

    def test_product_scan_source_length_1(self):
        source = 'a' * 40
        self.product_scan.source = source
        
        with self.assertRaises(ValidationError):
            self.product_scan.full_clean()