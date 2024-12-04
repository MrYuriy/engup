from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (if you have routers)
    from app.routers import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}

    return app
