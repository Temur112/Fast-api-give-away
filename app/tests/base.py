from cgi import test
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from db.database import Base, get_db
from models import user
from utils.utils import get_hashed_password

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

def create_test_user():
    db = TestSessionLocal()
    password = get_hashed_password("dpassword")
    testUSer = user.User(
        "dummy@email.com",
        "dummyusername",
        "dfirstname",
        "dlastname",
        "123456789",
        password
    )
    db.add(testUSer)
    db.commit()
    db.close()

def isUserExists()->bool:
    db = TestSessionLocal()
    testuser = db.query(user.User).filter(user.User.email == "dummy@email.com").first()
    if testuser is None:
        return False
    return True
    

class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        if not isUserExists():

            create_test_user()

    @classmethod
    def tearDownClass(cls) -> None:
        Base.metadata.drop_all(bind=engine)


