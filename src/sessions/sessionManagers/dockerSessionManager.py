import docker
import time

from ..brightsideSession import BrightsideSession
from .abstractSessionManager import AbstractSessionManager

class DockerSessionManager(AbstractSessionManager):
    def __init__(self):
        self._docker_client = docker.from_env()

    def setup_host(self, request):
        """
        Starts a browser container 

            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: The Brightside session
        """
        
        container_settings = {
            "image": f"selenium/standalone-chrome:latest",
            "detach": True
        }

        container = self._docker_client.containers.run(**container_settings)
        container = self._wait_for_container_status_running(container.id)
        return self._container_to_brightside_session(container)

    def terminate_host(self, container_id):
        """
        Deletes the Docker container
        The container ID is extracted from the session ID and the container is removed

            :param container_id: The session ID of the session to delete
            :type container_id: string
            :return: The response from the Selenium Grid hub

        """
        container = self._docker_client.containers.get(container_id)
        container.stop()
        container.remove()
    
    def find_host(self, container_id): 
        """
        Find a Docker container by ID and return it's info

            :param container_id: The ID of the container to find
            :type container_id: string
            :return: The Brightside session
        """
        containers = self._docker_client.containers.list(filters={"id": container_id})
        if len(containers) == 0:
            return None
        return self._container_to_brightside_session(containers[0])

    def _container_to_brightside_session(self, container): 
        """
        Converts a Docker container to a Brightside session

            :param container: The Docker container object to convert
            :type container: Docker container object
            :return: The Brightside session
        """
        container_info = container.attrs

        # Extract the IP address for the "bridge" network interface
        network_settings = container_info['NetworkSettings']
        ip_address = network_settings['Networks']['bridge']['IPAddress']
        return BrightsideSession(container.id, f"http://{ip_address}:4444")

    def _wait_for_container_status_running(self, container_id, timeout_seconds=30):
        """
        Wait for a pod to be running

            :param timeout: The timeout in seconds
            :type timeout: int
            :return: V1Pod
        """

        start_time = time.time()
        while True:
            try:
                container = self._docker_client.containers.get(container_id)
                container_info = container.attrs

                if container_info['State']['Status'] == "running":
                    return container

                if time.time() - start_time > timeout_seconds:
                    break

            except docker.errors.NotFound as e:
                print(f"Error getting pod status: {e}")

            time.sleep(1)

        raise TimeoutError(
            f"Timeout waiting for container {container_id} to reach Running state."
        )
