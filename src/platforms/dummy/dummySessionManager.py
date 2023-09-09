from src.platforms.abstractSessionManager import AbstractSessionManager


class DummySessionManager(AbstractSessionManager):
    """
    Session manager for the debug purpose
    """

    def create_session(self, request):
        """
        Sends a POST request to the Selenium Grid hub to create a new session and returns the response

          :param request: The request object from the Flask app
          :type request: Flask request object
          :return: Dummy response
        """

        return {"value": {"sessionId": "dummy_session_id"}}

    def proxy_requests(self, session_id, path, request):
        """
        Proxy requests to the Selenium Grid hub

            :param sessionId: The session ID of the session to proxy the request to
            :type sessionId: string
            :param path: The path to proxy the request to
            :type path: string
            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: Dummy response with the request data

        """

        return {
            "value": {
                "proxy_request": f"{request.method} {path} {request.data.decode('utf-8')}"
            }
        }

    def delete_session(self, session_id, request):
        """
        Deletes the session

            :param sessionId: The session ID of the session to delete
            :type sessionId: string
            :return: Dummy response
        """

        return {"value": "deleted session"}
