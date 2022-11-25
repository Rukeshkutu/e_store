from django.test import TestCase

from store.models import *

class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug = 'django')
        
    def test_category_model_entry(self):
        #test category model data insertion/type/field attributes
        
        data = self.data1
        self.assertTrue(isinstance(data,Category))