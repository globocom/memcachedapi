from flask import Flask

MEMCACHED = "127.0.0.1:11211"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/resources", methods=["POST"])
def add_instance():
    return "", 201


@app.route("/resources/<name>/host/<host>", methods=["DELETE"])
def remove_instance(name, host):
    return "", 200


@app.route("/resources/<name>", methods=["POST"])
def bind(name):
    return "", 201


if __name__ == "__main__":
    app.run()
