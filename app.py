import argparse

from flask import Flask, request
from src.platforms.platformFactory import PlatformFactory
from waitress import serve


def main():
    app = Flask(__name__)

    args = parse_args()

    platform = PlatformFactory.platformFor(args.platform)

    @app.route("/session", methods=["POST"])
    def create_session():
        return platform.create_session(request)

    @app.route("/session/<session_id>", methods=["DELETE"])
    def delete_session(session_id):
        return platform.delete_session(session_id, request)

    @app.route(
        "/session/<session_id>/<path:path>", methods=["GET", "POST", "DELETE", "PUT"]
    )
    def proxy_requests(session_id, path):
        return platform.proxy_requests(session_id, path, request)

    if args.debug:
        app.run(debug=True, host=args.host, port=args.port)
    else: 
        serve(app, host=args.host, port=args.port)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Brightside, the Selenium Grid in Kubernetes"
    )
    parser.add_argument("--platform", default="k8s", help="Platform to use (default: k8s)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to listen on (default: localhost)")
    parser.add_argument("--port", default=4444, help="Port to listen on (default: 4444)")
    parser.add_argument("--debug", action='store_true', default=False, help="Run server in debug mode (default: False)")
    # parser.set_defaults(debug=False)
    return parser.parse_args()


if __name__ == "__main__":
    main()
