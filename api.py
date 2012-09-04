from flask import Flask


app = Flask(__name__)


@app.route("/resources", methods=["POST"])
def add_instance():
    return "", 201


if __name__ == "__main__":
    app.run()
