import pytest 
import sys
from pathlib import Path
from flask_jwt_extended import decode_token
import uuid

# Add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))


from app import create_app, db
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    
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
        res = client.post("/api/v1/auth/login/", json={
            "email": email,
            "password": password,
        })
        token = res.json["tokens"]["access"]
        
        decoded = decode_token(token)
        identity_str = decoded.get("sub")
             
        # convert identity to uuid
        try:
            user_id = uuid.UUID(identity_str)
        except Exception:
            user_id = identity_str
            
        client.environ_base["HTTP_IDENTITY_UUID"] = str(user_id)
        
        return {"Authorization": f"Bearer {token}"}
    return _login



