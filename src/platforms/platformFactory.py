from .k8s.k8sSessionManager import K8SSessionManager
from .dummy.dummySessionManager import DummySessionManager
from .seleniumgrid.seleniumGridSessionManager import SeleniumGridSessionManager
from .docker.dockerSessionManager import DockerSessionManager

class PlatformFactory: 
    def platformFor(platform): 
        if platform == "k8s":
            return K8SSessionManager()
        elif platform == "selenium_grid":
            # TODO: Parameterize the Selenium Grid URL
            return SeleniumGridSessionManager("http://localhost:4444")
        elif platform == "docker":
            return DockerSessionManager()
        elif platform == "dummy":
            return DummySessionManager()