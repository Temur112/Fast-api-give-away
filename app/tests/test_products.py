import unittest
from base import BaseTest, TestSessionLocal


class TestProducts(BaseTest):

    __tablename__ = "items"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.db = TestSessionLocal()

    def tearDown(self):
        self.db.close()

    
    def test_add_products(self):
        ''' passes when authorized user adds product'''
        self.assertTrue(True)
    
    def test_add_product_without_authorization(self):
        '''fails when user adds product without authariation'''
        self.assertTrue(True)
    
    def test_updating_product_details(self):
        '''passes when authorized user updates user details'''
        self.assertTrue(True)
    
    def test_upddate_products_without_authorization(self):
        '''fails when unauthorized user tries to update product details'''
        self.assertTrue(True)