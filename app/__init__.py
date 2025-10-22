from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Initialisation des extensions

# SqlAlchemy permet de gérer la base de données
db = SQLAlchemy()
# Migrate permet de gérer les migrations de la base de données
migrate = Migrate()


# fontion de création de l'application
def create_app():

    # chargement des variables d'environnement
    load_dotenv()

    # Création de l'application Flask
    app = Flask(__name__)

    # Configuration de l'application avec les variables d'environnement
    # Clé secret pour le token
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
    # Configuration de la connection à la base de données
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    # Désactivation du suivi des modifications de SQLAlchemy ( reduit la consommation de mémoire)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initalisation des extensions avec l'application
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import des models
    from app.models import User, Deck
    from app.models import Card, Qa, AnswerQcm, Gapfill, Image, Qcm

    # # Import & Enregistrement des blueprints
    # from app.routes.todo_routes import todo_bp
    # from app.routes.user_routes import user_bp

    # app.register_blueprint(todo_bp)
    # app.register_blueprint(user_bp)

    return app
