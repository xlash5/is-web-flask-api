def home_route(app):
    @app.route("/", methods=["GET"])
    def home():
        return {"msg": "Hello World"}
