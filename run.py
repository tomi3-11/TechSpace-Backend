from app import create_app, db
from dotenv import load_dotenv
import os

load_dotenv(".env")

if os.environ.get("FLASK_ENV") == "production":
    load_dotenv(".env.prod", override=True)

app = create_app()

@app.cli.command("create-db")
def create_db():
    """Create all the tables."""
    with app.app_context():
        db.create_all()
        print("Database Tables created.")


if __name__ == "__main__":
    app.run(debug=True)
