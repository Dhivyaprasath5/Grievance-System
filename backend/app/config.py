import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-supersecretkey")

    # Use SQLite for local development (easier setup, no password needed)
    # To use MySQL, set USE_MYSQL=true in .env and configure DB credentials
    use_mysql = os.getenv("USE_MYSQL", "false").lower() == "true"
    
    if use_mysql:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
    else:
        # SQLite database file will be created in the backend directory
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "grievance.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
