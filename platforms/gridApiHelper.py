import requests

class GridHelper: 
    def api_request(url, request): 
        return requests.request(request.method, url, data=request.data, headers=request.headers).json()