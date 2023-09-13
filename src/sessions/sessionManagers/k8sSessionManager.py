import logging
import time

from uuid import uuid1
from kubernetes import client, config

from ..brightsideSession import BrightsideSession
from .abstractSessionManager import AbstractSessionManager

class K8SSessionManager(AbstractSessionManager):
    def __init__(self) -> None:
        config.load_incluster_config()
        self.api_instance = client.CoreV1Api()
        self.namespace = "default"  # TODO: Make this configurable

    def setup_host(self, request) -> BrightsideSession:
        """
        Create a browser pod

            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: The BrightsideSession object
        """

        name = uuid1().hex

        pod_spec = client.V1Pod(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name=name,
                        # TODO: Add support for custom images and capabilities
                        image=f"selenium/standalone-chrome:latest",
                        ports=[
                            client.V1ContainerPort(container_port=4444),
                            client.V1ContainerPort(container_port=7900),
                        ],
                    )
                ]
            ),
        )

        pod = self.api_instance.create_namespaced_pod(self.namespace, pod_spec)
        logging.info(f"Started pod {pod.metadata.name}")
        pod = self.wait_for_pod_status_running(name)

        return BrightsideSession(name, f"http://{pod.status.pod_ip}:4444")

    def terminate_host(self, pod_name) -> None:
        """
        Remove a browser pod

            :param containerId: The ID of the container to remove
            :type containerId: string
            :return: None
        """

        logging.info(f"Removing pod {pod_name}")
        self.api_instance.delete_namespaced_pod(pod_name, self.namespace)
        logging.info(f"Pod {pod_name} removed")

    def find_host(self, pod_name) -> BrightsideSession:
        """
        Find a browser pod by pod ID and return it's info

            :param host_id: The ID of the pod to find
            :type host_id: string
            :return: The Brightside session
        """
        logging.info(f"Searching for pod {pod_name}")
        pod_list = self.api_instance.list_namespaced_pod(self.namespace)

        for pod in pod_list.items:
            if pod.metadata.name == pod_name:
                logging.info(f"Found pod {pod_name} with IP {pod.status.pod_ip}")
                return BrightsideSession(pod_name, f"http://{pod.status.pod_ip}:4444")

        return None

    def wait_for_pod_status_running(self, pod_name, timeout_seconds=600) -> client.V1Pod:
        """
        Wait for a pod to be running

            :param timeout: The timeout in seconds
            :type timeout: int
            :return: V1Pod
        """

        logging.info(f"Waiting for pod {pod_name} to reach Running state")
        start_time = time.time()
        while True:
            try:
                pod = self.api_instance.read_namespaced_pod(
                    name=pod_name, namespace=self.namespace
                )

                logging.info(f"Pod {pod_name} status: {pod.status.phase}")
                if pod.status.phase == "Running":
                    return pod

                if time.time() - start_time > timeout_seconds:
                    break

            except client.exceptions.ApiException as e:
                raise RuntimeError(f"Error getting pod status: {e}")

            time.sleep(1)

        logging.info(f"Pod {pod_name} did not reach Running state in {timeout_seconds} seconds, deleting pod")
        self.terminate_host(pod_name)
        raise TimeoutError(
            f"Timeout waiting for pod {pod_name} in namespace {self.namespace} to reach Running state."
        )
