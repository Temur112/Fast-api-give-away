from utils import utils
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm  import sessionmaker
from main import app
from db.database import Base, get_db
from models import user


TEST_DB_URL = "sqlite:///./test.db"


engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


Base.metadata.create_all(bind = engine)

client = TestClient(app)



class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

        cls.engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
        cls.TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

        cls.db = cls.TestingSessionLocal()



        cls.dUser = user.User()
        cls.dUser.email = "dummy@email.com"
        cls.dUser.username = "dummyusername"
        cls.dUser.firstname = "dfirstname"
        cls.dUser.lastname = "dlastname"
        cls.dUser.password = utils.get_hashed_password("dpassword")

        cls.db.add(cls.dUser)
        cls.db.commit()

    @classmethod 
    def tearDownClass(cls):
        cls.db.query(user.User).delete()
        cls.db.commit()
        cls.db.close()
        Base.metadata.drop_all(bind=cls.engine)
        cls.engine.dispose()

    def setUp(self):
        self.db = TestSessionLocal()
        # create dummy user


    def tearDown(self):

        self.db.close()

    def test_register_user(self):
        response = client.post(
            "/auth/register",
            json = {
                    "username": "testusername",
                    "email": "test@example.com",
                    "firstname": "testfirstname",
                    "lastname": "string",
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
        response = client.post(
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
        response = client.post(
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

        response = client.put(
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
        response = client.put(
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