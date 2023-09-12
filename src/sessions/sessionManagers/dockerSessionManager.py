import docker
import time
import logging

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
        logging.info(f"Started container {container.id}")
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
        logging.info(f"Stopping container {container.id}")
        container.stop()
        logging.info(f"Removing container {container.id}")
        container.remove()
        logging.info(f"Container {container.id} removed")
    
    def find_host(self, container_id): 
        """
        Find a Docker container by ID and return it's info

            :param container_id: The ID of the container to find
            :type container_id: string
            :return: The Brightside session
        """
        logging.info(f"Searching for container {container_id}")
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
        logging.info(f"Container {container.id} has IP address {ip_address}")
        return BrightsideSession(container.id, f"http://{ip_address}:4444")

    def _wait_for_container_status_running(self, container_id, timeout_seconds=600):
        """
        Wait for a pod to be running

            :param timeout: The timeout in seconds
            :type timeout: int
            :return: V1Pod
        """

        logging.info(f"Waiting for container {container_id} to reach Running state")
        start_time = time.time()
        while True:
            try:
                container = self._docker_client.containers.get(container_id)
                container_info = container.attrs
                container_status = container_info['State']['Status']
                logging.info(f"Container {container_id} has status {container_status}")

                if container_info['State']['Status'] == "running":
                    return container

                if time.time() - start_time > timeout_seconds:
                    break

            except docker.errors.NotFound as e:
                raise RuntimeError(f"Container {container_id} not found")

            time.sleep(1)

        logging.info(f"Container {container_id} did not reach Running state in {timeout_seconds} seconds, deleting container")
        self.terminate_host(container_id)
        raise TimeoutError(
            f"Timeout waiting for container {container_id} to reach Running state."
        )
