from platforms.abstractSessionManager import AbstractSessionManager
from utils.network_utils import get_free_port
from utils.selenium_grid_utils import wait_for_grid_4_availability

import requests
import docker


class DockerSessionManager(AbstractSessionManager):
    def __init__(self):
        self.docker_client = docker.from_env()
        self.containers = {}

    def create_session(self, request):
        """
        Starts a browser container and starts session in it

          :param request: The request object from the Flask app
          :type request: Flask request object
          :return: The response from the Selenium Grid hub
        """

        selenium_grid_port = get_free_port()
        selenium_grid_url = f"http://localhost:{selenium_grid_port}"
        no_vnc_port = get_free_port()

        container_settings = {
            "image": "selenium/standalone-chrome:latest",  # TODO: Parameterize the image
            "detach": True,
            "ports": {"4444/tcp": selenium_grid_port, "7900/tcp": no_vnc_port},
        }

        container = self.docker_client.containers.run(**container_settings)
        self.containers[container.id] = selenium_grid_url

        wait_for_grid_4_availability(selenium_grid_url)
        
        response = requests.post(f"{selenium_grid_url}/session", json=request.json)

    def proxy_requests(self, sessionId, path, request):
        """
        Proxy requests to the container

            :param sessionId: The session ID of the session to proxy the request to
            :type sessionId: string
            :param path: The path to proxy the request to
            :type path: string
            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: The response from the Selenium Grid hub

        """
        pass

    def delete_session(self, sessionId):
        """
        Deletes the Docker container

            :param sessionId: The session ID of the session to delete
            :type sessionId: string
            :return: The response from the Selenium Grid hub

        """

        pass
