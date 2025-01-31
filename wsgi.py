from game import app

# The wsgi.py file is a simple script that imports the app object from game.py and runs it. This is the entry point for the WSGI server, which is the server that will run the Flask application. This script is used by the WSGI server to start the application.
if __name__ == '__main__':
    app.run()
    