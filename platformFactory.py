from platforms.seleniumGridSessionManager import SeleniumGridSessionManager

class PlatformFactory: 
    def platformFor(platform): 
        # TODO: Implement Kubernetes platform here
        if platform == "kubernetes":
            pass
        elif platform == "selenium_grid":
            # TODO: Parameterize the Selenium Grid URL
            return SeleniumGridSessionManager('http://localhost:4444')