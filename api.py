from flask import Flask


app = Flask(__name__)


@app.route("/resources", methods=["POST"])
def add_instance():
    return "", 201


@app.route("/resources/<name>/host/<host>", methods=["DELETE"])
def remove_instance(name, host):
    return "", 200


if __name__ == "__main__":
    app.run()
