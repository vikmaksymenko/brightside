import requests
import time

def wait_for_grid_4_availability(grid_url, timeout=30):
    """
    Waits for the Selenium Grid 4 hub to be available

        :param grid_url: The URL of the Selenium Grid hub
        :type grid_url: string
        :param timeout: The timeout in seconds  (Default: 30)
        :type timeout: int  
        :return: None
    """

    for i in range(timeout):
        if is_grid_4_available(grid_url):
            return True
        time.sleep(1)

    raise Exception(f"Timed out waiting for Selenium Grid 4 to be available at {grid_url}")

    
def is_grid_4_available(grid_url):
    """
    Checks if the Selenium Grid hub is available

        :param grid_url: The URL of the Selenium Grid hub
        :type grid_url: string
        :return: True if the Selenium Grid hub is available, False otherwise
    """

    try:
        response = requests.get(f"{grid_url}/status")
        return response.status_code == 200 and response.json()["value"]["ready"]
    except:
        return False