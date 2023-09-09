from src.platforms.abstractSessionManager import AbstractSessionManager
from src.platforms.gridApiHelper import GridHelper

class SeleniumGridSessionManager(AbstractSessionManager):

    def __init__(self, url):
        self.url = url

    def create_session(self, request):
        """
        Sends a POST request to the Selenium Grid hub to create a new session and returns the response

          :param request: The request object from the Flask app
          :type request: Flask request object
          :return: The response from the Selenium Grid hub
        """

        return GridHelper.api_request(self.url + "/session", request)


    def proxy_requests(self, session_id, path, request):
        """
        Proxy requests to the Selenium Grid hub

            :param sessionId: The session ID of the session to proxy the request to
            :type sessionId: string
            :param path: The path to proxy the request to
            :type path: string
            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: The response from the Selenium Grid hub

        """

        return GridHelper.api_request(f"{self.url}/session/{session_id}/{path}", request)


    def delete_session(self, session_id, request):
        """
        Deletes the session from the Selenium Grid hub

            :param sessionId: The session ID of the session to delete
            :type sessionId: string
            :return: The response from the Selenium Grid hub

        """

        return GridHelper.api_request(f"{self.url}/session/{session_id}", request)

    