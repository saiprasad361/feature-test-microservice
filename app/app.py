from flask import Flask, jsonify
import os

app = Flask(__name__)

FEATURE_VERSION = os.getenv("FEATURE_VERSION", "v1")
BUGFIX_ENABLED = os.getenv("BUGFIX_ENABLED", "false")

@app.route("/health")
def health():
    return jsonify(status="UP")

@app.route("/version")
def version():
    return jsonify(version=FEATURE_VERSION)

@app.route("/bugfix")
def bugfix():
    if BUGFIX_ENABLED.lower() == "true":
        return jsonify(message="Bug fixed successfully")
    else:
        return jsonify(message="Known bug still present"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

