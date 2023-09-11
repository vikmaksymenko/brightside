class BrightsideSession: 
    def __init__(self, host_id, grid_url, metadata = {}):
        """
        Data class for a Brightside session
        """

        self._host_id = host_id
        self._grid_url = grid_url
        self._metadata = metadata

    @property
    def host_id(self):
        """
        The ID of the Brightside session
        """
        return self._host_id
    
    @property
    def grid_url(self):
        """
        The URL of the Selenium Grid hub
        """
        return self._grid_url
    
    @property
    def metadata(self):
        """
        Metadata of the Brightside session
        """
        return self._metadata
