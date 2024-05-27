from utils import utils
from models import user
from base import BaseTest, TestSessionLocal
import unittest



class TestAuth(BaseTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        

    @classmethod 
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.db = TestSessionLocal()


    def tearDown(self):

        self.db.close()

    def test_register_user(self):
        response = self.client.post(
            "/auth/register",
            json = {
                    "username": "testusername",
                    "email": "test@example.com",
                    "firstname": "testfirstname",
                    "lastname": "string",
                    "phone_number": "123456789",
                    "password": "string"
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["username"], "testusername")
        self.assertEqual(data["firstname"], "testfirstname")
        self.assertEqual(data["lastname"], "string")
        self.assertFalse(data["is_banned"])

    def test_login_with_valid_credientials(self):
        '''Passes with correct credientials'''
        response = self.client.post(
            "/auth/login",
            data = {
                "username": "dummy@email.com",
                "password": "dpassword"
            }
        )

        # print(response.json()) #debugging purpose
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['message'], "Login Successful")
        self.__class__.token = data["token"]
        

    def test_login_with_invalid_credientials(self):
        '''Fails with invalid credentials'''
        response = self.client.post(
            "/auth/login",
            data = {
                "username": "test@example.com",
                "password": "string2"
            }
        )

        self.assertEqual(response.status_code, 401)
        data = response.json()
        # print(data)  #Debugging purpose
        self.assertEqual(data["detail"], "Incorrect email or password")

    def test_update_user_credientials(self):
        '''test changing user credentials and does not return password'''
        if not hasattr(self.__class__, 'token'):
            self.skipTest("someting went wrong")

        header = {"Authorization": f"Bearer {self.__class__.token}"}

        response = self.client.put(
            "/auth/updateProfile",
            headers = header,

            json = {
                "firstname": "UpdatedFirstName",
                "lastname": "UpdatedLastName",
                "username": "updateduser",
            }
            
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["firstname"], "UpdatedFirstName")
        self.assertEqual(data["lastname"], "UpdatedLastName")
        self.assertEqual(data["username"], "updateduser")
        # self.assertTrue(utils.verify_password("updatedpassword", data["password"])) #wrong part
        self.assertNotIn('password', data)


    def test_fails_update_profile_without_authentication(self):
        '''fails test case without authentication'''
        response = self.client.put(
            "/auth/updateProfile",
            json = {
                "firstname": "UpdatedFirstName",
                "lastname": "UpdatedLastName",
                "username": "updateduser",
            
            }
        )
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        

if __name__ == "__main__":
    unittest.main()