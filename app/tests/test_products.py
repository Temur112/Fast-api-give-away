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
            cls.product_id = 0
        else:
            raise Exception("Authentcation failed during test setup")
        


    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
        

    def setUp(self):
        self.db = TestSessionLocal()
        self.product_id = 0
        


    def tearDown(self):
        self.db.close()

    
    def test_1_add_products(self):
        ''' passes when authorized user adds product'''
        response = self.client.post(
            f"/products/addproduct/",
            headers = self.__class__.header,
            json = {
                "title": "Phone",
                "description": "phone description",
                "price": 12,
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("title"), "Phone")
        self.assertEqual(data.get("description"), "phone description")
        self.assertEqual(data.get("price"), 12)
       
    
    
    def test_2_add_product_without_authorization(self):
        '''fails when user adds product without authariation'''
        response = self.client.post(
            "/products/addproduct",
            json = {
                "title": "Phone",
                "description": "phone description",
                "price": 12,
            }
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data.get("detail"), "Not authenticated")
    
    def test_3_updating_product_details_by_id(self):
        '''passes when authorized user updates user details'''
        response = self.client.post(
            "/products/addproduct",
            headers = self.__class__.header,
            json = {
                "title": "Phone2",
                "description": "phone2 description",
                "price": 20,
            }
        )
        data = response.json()
        id = data.get("id")

        response = self.client.put(
            f"/products/update/{id}",
            headers = self.__class__.header,
            json = {
                "title": "New Phone",
                "description": "new description",
                "price": 15,
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # print(data) # debugging purposes
        self.assertEqual(data.get("title"), "New Phone")
        self.assertEqual(data.get("description"), "new description")
        self.assertEqual(data.get("price"), 15)
    
    def test_4_upddate_products_without_authorization(self):
        '''fails when unauthorized user tries to update product details'''
        response = self.client.put(
            f"/products/update/1",
            json = {
                "title": "New Phone",
                "description": "new description",
                "price": float(15.5),
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_5_get_all_products(self):
        '''Returns all products'''
        response = self.client.get(
            "/products/getall",
        )
        
        n = len(self.db.query(Item).all())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), n)


    def test_6_get_users_products(self):
        '''returns products which user added'''
        response = self.client.get(
            "products/myproducts",
            headers = self.__class__.header,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        n = len(self.db.query(Item).filter(Item.owner_id == 1).all())
        self.assertEqual(len(data), n)

    def test_7_get_product_details_by_id(self):
        '''returns detailed information of product to authenticates user'''
        response = self.client.post(
            "/products/addproduct",
            headers = self.__class__.header,
            json = {
                "title": "Phone test 7",
                "description": "phone test 7 description",
                "price": 7,
            }
        )

        id = response.json().get("id")
        self.__class__.product_id = id

        response = self.client.get(
            f"/products/getproduct/{id}",
            headers = self.__class__.header
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("title"), "Phone test 7")

    def test_8_delete_product_by_id(self):
        '''users can deelte products which owns by themselves'''

        response = self.client.delete(
            f"/products/deleteproduct/{self.__class__.product_id}",
            headers = self.__class__.header,
        )

        self.assertEqual(response.status_code, 200)

    def test_9_delete_products_without_authentication(self):
        '''fails when user tries to delete products without authentication'''
        response = self.client.delete(
            f"/products/deleteproduct/1"
        )

        self.assertEqual(response.status_code, 401)


    def test_10_get_product_details_without_authentication(self):
        '''returns products by id'''

        response = self.client.post(
            "/products/addproduct",
            headers = self.__class__.header,
            json = {
                "title": "test 10",
                "description": "phone test 7 description",
                "price": 10,
            }
        )

        id = response.json().get("id")

        response = self.client.get(
            f"/products/getproduct/{id}",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        # print(data)
        item = self.db.query(Item).filter(Item.id == id).first()
        self.assertEqual(data.get("title"), item.title)
        # more checks can be added

    ### Test cases will continue from here