from flask import Flask

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index)
    
    def index(self):
        return "Index"

if __name__ == '__main__':
    app = FlaskApp()

    app.app.run("0.0.0.0", 8080, debug=True)