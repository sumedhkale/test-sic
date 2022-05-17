from app import create_app

app = create_app()

@app.route("/")
def hello():
    return "Hello! This is a basic Flask app. "


if __name__ == "__main__":
    app.run("0.0.0.0")
