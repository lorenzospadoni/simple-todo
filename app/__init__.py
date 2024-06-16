from flask import Flask

def registerExtensions(flask_application: Flask):
    with flask_application.app_context():
        import extensions, auth, views

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

