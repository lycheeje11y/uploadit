from web.web import Config

if __name__ == "__main__":
    config = Config()
    config.flask_app.run(host="0.0.0.0", port=1212, debug=True)
