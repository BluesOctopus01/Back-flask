from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_cors import CORS
from dotenv import load_dotenv
from app.configs.config import TestConfig
import os

# Initialisation des extensions

# SqlAlchemy permet de gérer la base de données
db = SQLAlchemy()
# Migrate permet de gérer les migrations de la base de données
migrate = Migrate()


# fontion de création de l'application
def create_app(config_class=None):

    # chargement des variables d'environnement
    load_dotenv()

    # Création de l'application Flask
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URL", "sqlite:///app.db"
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initalisation des extensions avec l'application
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import des models
    from app.models.user_models.user import User

    from app.models.cards_models.card_answer_qcm import AnswerQcm
    from app.models.cards_models.card_base import Card
    from app.models.cards_models.card_gapfill import Gapfill
    from app.models.cards_models.card_image import Image
    from app.models.cards_models.card_qa import Qa
    from app.models.cards_models.card_qcm import Qcm

    from app.models.deck import Deck

    from app.models.tags import Tag, TagDeck

    # # Import & Enregistrement des blueprints
    # from app.routes.todo_routes import todo_bp
    from app.routes.user_route import user_bp
    from app.routes.deck_route import deck_bp
    from app.routes.card_route import card_bp
    from app.routes.tag_route import tag_bp

    # app.register_blueprint(user_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(deck_bp)
    app.register_blueprint(card_bp)
    app.register_blueprint(tag_bp)

    return app
