from flask import Flask, request

from src.platforms.platformFactory import PlatformFactory

app = Flask(__name__)

platform = PlatformFactory.platformFor("k8s")

@app.route("/session", methods=["POST"])
def create_session():
    return platform.create_session(request)

@app.route("/session/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    return platform.delete_session(session_id, request)

@app.route("/session/<session_id>/<path:path>", methods=["GET", "POST", "DELETE", "PUT"])
def proxy_requests(session_id, path):
    return platform.proxy_requests(session_id, path, request)

if __name__ == "__main__":
    app.run(debug=True)
