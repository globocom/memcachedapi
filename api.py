import os

import memcache
from flask import Flask, jsonify

MEMCACHED = os.environ.get("MEMCACHED", "127.0.0.1:11211")
PUBLIC_HOST = os.environ.get("PUBLIC_HOST", MEMCACHED)

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
    out = jsonify(MEMCACHED=app.config["PUBLIC_HOST"])
    return out, 201


@app.route("/resources/<name>", methods=["DELETE"])
def unbind(name):
    return "", 200


@app.route("/resources/<name>/status", methods=["GET"])
def status(name):
    client = memcache.Client([app.config["MEMCACHED"]])
    if client.servers[0].connect() == 1:
        return "", 204
    return "", 500


if __name__ == "__main__":
    app.run()
