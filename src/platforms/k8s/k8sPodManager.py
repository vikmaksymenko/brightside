import time
from uuid import uuid1
from kubernetes import client, config


class K8sPodManager:
    def __init__(self):
        config.load_incluster_config()
        self.api_instance = client.CoreV1Api()

    def create_browser_pod(
        self, browser_name="chrome", version="latest", namespace="default"
    ):
        """
        Create a browser pod

            :param browserName: The name of the browser to create the pod for
            :type browserName: string
            :param version: The version of the browser to create the pod for
            :type version: string
            :param namespace: The namespace to create the pod in
            :type namespace: string
            :return: The tuple of the container ID and the grid URL (pod IP + port)
        """

        name = uuid1().hex

        pod_spec = client.V1Pod(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name=name,
                        image=f"selenium/standalone-{browser_name}:{version}",
                        ports=[
                            client.V1ContainerPort(container_port=4444),
                            client.V1ContainerPort(container_port=7900),
                        ],
                    )
                ]
            ),
        )

        pod = self.api_instance.create_namespaced_pod(namespace, pod_spec)

        pod = self.wait_for_pod_status_running(name, namespace)

        return (name, f"http://{pod.status.pod_ip}:4444")

    def delete_browser_pod(self, pod_name, namespace="default"):
        """
        Remove a browser pod

            :param containerId: The ID of the container to remove
            :type containerId: string
            :return: None
        """

        self.api_instance.delete_namespaced_pod(pod_name, namespace)

    def wait_for_pod_status_running(
        self, pod_name, namespace="default", timeout_seconds=30
    ):
        """
        Wait for a pod to be running

            :param timeout: The timeout in seconds
            :type timeout: int
            :return: V1Pod
        """

        start_time = time.time()
        while True:
            try:
                pod = self.api_instance.read_namespaced_pod(
                    name=pod_name, namespace=namespace
                )

                if pod.status.phase == "Running":
                    return pod

                if time.time() - start_time > timeout_seconds:
                    break

            except client.exceptions.ApiException as e:
                print(f"Error getting pod status: {e}")

            time.sleep(1)

        raise TimeoutError(
            f"Timeout waiting for pod {pod_name} in namespace {namespace} to reach Running state."
        )
