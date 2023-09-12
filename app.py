import argparse
import logging

from flask import Flask, request
from waitress import serve
from paste.translogger import TransLogger


from src.sessions.sessionRouter import SessionRouter

def main():
    args = parse_args()

    log_level = getattr(logging, args.log_level)
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] [%(name)s] [%(process)d] [%(thread)d] - %(message)s',
        level=log_level
    )

    app = Flask(__name__)

    session_router = SessionRouter(args.platform)
 
    @app.route("/session", methods=["POST"])
    def create_session():
        return session_router.create_session(request)

    @app.route("/session/<session_id>", methods=["DELETE"])
    def delete_session(session_id):
        return session_router.delete_session(session_id, request)

    @app.route(
        "/session/<session_id>/<path:path>", methods=["GET", "POST", "DELETE", "PUT"]
    )
    def proxy_requests(session_id, path):
        return session_router.proxy_requests(session_id, path, request)

    if args.debug:
        app.run(debug=True, host=args.host, port=args.port)
    else: 
        # serve(app, host=args.host, port=args.port)
        serve(TransLogger(app, setup_console_handler=False), host=args.host, port=args.port)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Brightside, the Selenium Grid in Kubernetes"
    )
    parser.add_argument("--platform", default="k8s", help="Platform to use (default: k8s)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to listen on (default: localhost)")
    parser.add_argument("--port", default=4444, help="Port to listen on (default: 4444)")
    parser.add_argument("--debug", action='store_true', default=False, help="Run server in debug mode (default: False)")
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    default='INFO', help='Set the log level (default: INFO)')
    return parser.parse_args()


if __name__ == "__main__":
    main()
