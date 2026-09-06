from flask import Flask
from config import Config
from models.audit_log import AuditLog
from controllers.auth_controller import auth_bp
from controllers.file_controller import file_bp
from models.policy import Policy
from models.file import File
from extensions import (
    db,
    migrate,
    login_manager
)

# Import models so Flask-Migrate can detect them
from models.user import User


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    app.register_blueprint(auth_bp)
    app.register_blueprint(file_bp)

    # Home route
    @app.route("/")
    def home():
        return "Sovereign Cloud Platform Running"

    return app


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)