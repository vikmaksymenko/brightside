from abc import ABC, abstractmethod

class AbstractSessionManager(ABC):
    @abstractmethod
    def create_session(self, request):
        """
        Prepares a browser session

          :param request: The request object from the Flask app
          :type request: Flask request object
          :return: The response from the Selenium Grid hub
        """
        pass
    
    @abstractmethod
    def proxy_requests(self, sessionId, path, request):
        """
        Proxy requests to the browser session

            :param sessionId: The session ID of the session to proxy the request to
            :type sessionId: string
            :param path: The path to proxy the request to
            :type path: string
            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: The response from the Selenium Grid hub

        """
        pass
    
    @abstractmethod
    def delete_session(self, session_id, request):
        """
        Deletes the session 

            :param sessionId: The session ID of the session to delete
            :type sessionId: string
            :return: The response from the Selenium Grid hub

        """
        pass
    