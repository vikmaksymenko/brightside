import requests
import time

class GridHelper: 
    empty_response = {
        "value": None,
    }

    def api_request(url, request): 
        response = requests.request(request.method, url, data=request.data, headers=request.headers).json()
        print(response)
        return response