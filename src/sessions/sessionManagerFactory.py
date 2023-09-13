from .sessionManagers.abstractSessionManager import AbstractSessionManager
from .sessionManagers.dockerSessionManager import DockerSessionManager
from .sessionManagers.k8sSessionManager import K8SSessionManager


class SessionManagerFactory:
    def platformFor(platform) -> AbstractSessionManager:
        """
        Returns the session manager for the given platform

            :param platform: The platform to return the session manager for
            :type platform: string
            :return: The session manager
        """
        if platform == "k8s":
            return K8SSessionManager()
        elif platform == "docker":
            return DockerSessionManager()
        else:
            raise ValueError(f"Unknown platform: {platform}")
