import pytest 
from app import create_app, db
from config import TestConfig


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)
    
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        
        
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    def _login(email, password):
        res = client.post("/api/v1/auth/login/", json=(
            "email": email,
            "password": password,
        ))
        token = res.json["access"]
        return {"Authorization": f"Bearer {token}"}
    return _login



