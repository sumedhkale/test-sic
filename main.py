from app import create_app
from markdown import markdown

app = create_app()


@app.route("/")
def hello():
    readme_file = open("README.md", "r")
    md_template_string = markdown(
        readme_file.read(), extensions=["fenced_code", "codehilite"]
    )
    return md_template_string


if __name__ == "__main__":
    app.run("0.0.0.0")
