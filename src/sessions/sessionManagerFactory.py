from .sessionManagers.dockerSessionManager import DockerSessionManager
from .sessionManagers.k8sSessionManager import K8SSessionManager

class SessionManagerFactory: 
    def platformFor(platform): 
        if platform == "k8s":
            return K8SSessionManager()
        elif platform == "docker":
            return DockerSessionManager()
        else:
            raise ValueError(f"Unknown platform: {platform}")
        pass