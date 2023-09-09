from .dockerContainerManager import DockerContainerManager
from ..abstractSessionManager import AbstractSessionManager
from ..gridApiHelper import GridHelper
from ...utils.selenium_grid_utils import wait_for_grid_4_availability

class DockerSessionManager(AbstractSessionManager):
    def __init__(self):
        self.containers = {}
        self.container_manager = DockerContainerManager()

    def create_session(self, request):
        """
        Starts a browser container and starts session in it. 
        Returns the response from the Selenium Grid hub with modified session ID
        Where session ID is a combination of container ID and session ID in the container

          :param request: The request object from the Flask app
          :type request: Flask request object
          :return: The response from the Selenium Grid hub
        """

        container_id, grid_url = self.container_manager.create_browser_container()
        self.containers[container_id] = grid_url

        wait_for_grid_4_availability(grid_url)

        response = GridHelper.api_request(grid_url + '/session', request)

        # TODO: Handle error response
        session_id = response['value']['sessionId']
        response['value']['sessionId'] = container_id + session_id

        return response


    def proxy_requests(self, session_id, path, request):
        """
        Proxy requests to the container. 
        The container ID is extracted from the session ID and the request is proxied to the container URL

            :param sessionId: The session ID of the session to proxy the request to
            :type sessionId: string
            :param path: The path to proxy the request to
            :type path: string
            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: The response from the Selenium Grid hub

        """
        
        container_id, browser_session_id = self.__parse_session_id(session_id)
        grid_url = self.containers[container_id]
        return GridHelper.api_request(f"{grid_url}/session/{browser_session_id}/{path}", request)

    def delete_session(self, session_id, request):
        """
        Deletes the Docker container
        The container ID is extracted from the session ID and the container is removed

            :param sessionId: The session ID of the session to delete
            :type sessionId: string
            :return: The response from the Selenium Grid hub

        """
        container_id = self.__parse_session_id(session_id)[0]
        self.container_manager.delete_browser_container(container_id)
        return GridHelper.empty_response
    
    def __parse_session_id(self, session_id):
        return (session_id[:64], session_id[64:])
