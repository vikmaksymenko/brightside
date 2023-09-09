from .seleniumgrid.seleniumGridSessionManager import SeleniumGridSessionManager
from .docker.dockerSessionManager import DockerSessionManager

class PlatformFactory: 
    def platformFor(platform): 
        # TODO: Implement Kubernetes platform here
        if platform == "kubernetes":
            pass
        elif platform == "selenium_grid":
            # TODO: Parameterize the Selenium Grid URL
            return SeleniumGridSessionManager('http://localhost:4444')
        elif platform == "docker":
            return DockerSessionManager()