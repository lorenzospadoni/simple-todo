from flask import Flask
from flask_cors import CORS

def registerExtensions(flask_application: Flask):
    with flask_application.app_context():
        import extensions, auth, views
        extensions.cors.init_app(flask_application, 
            supports_credentials=flask_application.config['CORS_SUPPORTS_CREDENTIALS'],
            redirect=flask_application.config['CORS_REDIRECT'],
            allow_headers=flask_application.config['CORS_ALLOW_HEADERS'],
            resources=flask_application.config['CORS_RESOURCES'])

def registerBlueprints(flask_application: Flask):
    pass

def createApp() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    registerExtensions(app)
    registerBlueprints(app)
    return app

if __name__=='__main__':
    app = createApp()
    app.run(debug=True)

