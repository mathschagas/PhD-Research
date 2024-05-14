import multiprocessing
from flask import Flask, jsonify

def create_app(name):
    app = Flask(name)

    @app.route('/health')
    def health():
        return jsonify(status='OK')

    return app

def run_app(name, route, message):
    app = create_app(name)

    @app.route(route)
    def view():
        return jsonify(message=message)

    app.run()

if __name__ == '__main__':
    multiprocessing.Process(target=run_app, args=(__name__, '/', 'Hello, World!')).start()
    multiprocessing.Process(target=run_app, args=(__name__, '/goodbye', 'Goodbye, World!')).start()