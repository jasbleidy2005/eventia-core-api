from flask import Flask
from flask_cors import CORS
from src.routes.event_routes import event_bp
from src.routes.participant_routes import participant_bp
from src.routes.attendance_routes import attendance_bp
from src.config.settings import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Registrar blueprints
    app.register_blueprint(event_bp)
    app.register_blueprint(participant_bp)
    app.register_blueprint(attendance_bp)
    
    @app.route('/')
    def health_check():
        return {'status': 'OK', 'message': 'Eventia Core API is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_ENV == 'development'
    )