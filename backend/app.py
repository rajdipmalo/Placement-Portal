import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail  
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from utils.timezone import ist_now

load_dotenv()

from models import db, User
from config import Config
from extensions import cache

jwt = JWTManager()
mail = Mail()  


def create_app():
    app = Flask(__name__)
    CORS(
        app,
        resources={r"/api/*": {"origins": [os.getenv("FRONTEND_URL")]}},
        supports_credentials=True
    )
    app.config.from_object(Config)


    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {"sslmode": "require"}
    }

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)  
    cache.init_app(app)

    from auth.routes import auth_bp
    from admin.routes import admin_bp
    from company.routes import company_bp
    from student.routes import student_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(company_bp, url_prefix='/api/company')
    app.register_blueprint(student_bp, url_prefix='/api/student')

    return app


app = create_app()


with app.app_context():
    db.create_all()

    admin_email = "malorajdip14@gmail.com"
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            email=admin_email,
            password=generate_password_hash("admin123"),
            role="admin",
            is_active=True,
            is_verified=True,  
            verified_at=ist_now()
        )
        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)