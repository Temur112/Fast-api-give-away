from base import BaseTest, TestSessionLocal
from models.item import Item

class TestProducts(BaseTest):

    __tablename__ = "items"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        response = cls.client.post(
            "/auth/login",
            data = {
                "username": "dummy@email.com",
                "password": "dpassword"
            }
        )
        if response.status_code == 200:
            token = response.json().get("token")
            cls.header = {"Authorization": f"Bearer {token}"}
        else:
            raise Exception("Authentcation failed during test setup")


    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
        

    def setUp(self):
        self.db = TestSessionLocal()
        


    def tearDown(self):
        self.db.close()

    
    def test_add_products(self):
        ''' passes when authorized user adds product'''
        response = self.client.post(
            "/products/addproduct",
            headers = self.__class__.header,
            json = {
                "title": "Phone",
                "description": "phone description",
                "price": float(12.5),
            }
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data.get("title"), "Phone")
        self.assertEqual(data.get("description"), "phone description")
        self.assertEqual(data.get("price"), 12.5)
        self.id = data.get("id")
    
    def test_add_product_without_authorization(self):
        '''fails when user adds product without authariation'''
        response = self.client.post(
            "/products/addproduct",
            json = {
                "title": "Phone",
                "description": "phone description",
                "price": float(12.5),
            }
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data.get("detail", "Validation error Could not validate credientials!"))
    
    def test_updating_product_details_by_id(self):
        '''passes when authorized user updates user details'''
        response = self.client.put(
            f"/products/update/{self.id}",
            headers = self.__class__.header,
            json = {
                "title": "New Phone",
                "description": "new description",
                "price": float(15.5),
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("title"), "New Phone")
        self.assertEqual(data.get("description"), "new description")
        self.assertEqual(data.get("price"), 15.5)
    
    def test_upddate_products_without_authorization(self):
        '''fails when unauthorized user tries to update product details'''
        response = self.client.put(
            f"/product/update/{self.id}",
            headers = self.__class__.header,
            json = {
                "title": "New Phone",
                "description": "new description",
                "price": float(15.5),
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_get_all_products(self):
        '''Returns all products'''
        response = self.client.get(
            "/product/get/all",
        )
        
        n = len(self.db.query(Item).all())
        self.assertEqual(response.status_code, 200)
        data = response
        self.assertEqual(len(data), n)


    def test_get_users_products(self):
        '''returns products which user added'''
        response = self.client.get(
            "products/myproducts",
            headers = self.__class__.header,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_delete_product_by_id(self):
        '''users can deelte products which owns by themselves'''

        response = self.client.delete(
            f"/products/delete/{self.id}",
            headers = self.__class__.header
        )

        self.assertEqual(response.status_code, 200)