import docker
from src.utils.network_utils import find_free_port


class DockerContainerManager:
    def __init__(self):
        self.docker_client = docker.from_env()

    def create_browser_container(self, browser_name="chrome", version="latest"):
        """
        Create a browser container

            :param browserName: The name of the browser to create the container for
            :type browserName: string
            :param version: The version of the browser to create the container for
            :type version: string
            :return: The tuple of the container ID and the container URL
        """

        selenium_grid_port = find_free_port()
        selenium_grid_url = f"http://localhost:{selenium_grid_port}"
        no_vnc_port = find_free_port()

        container_settings = {
            "image": f"selenium/standalone-{browser_name}:{version}",
            "detach": True,
            "ports": {"4444/tcp": selenium_grid_port, "7900/tcp": no_vnc_port},
        }

        # TODO: Add error handling here
        container = self.docker_client.containers.run(**container_settings)
        return (container.id, selenium_grid_url)

    def delete_browser_container(self, container_id):
        """
        Remove a browser container

            :param containerId: The ID of the container to remove
            :type containerId: string
            :return: None
        """

        container = self.docker_client.containers.get(container_id)
        container.stop()
        container.remove()
