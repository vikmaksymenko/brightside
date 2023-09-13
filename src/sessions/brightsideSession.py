class BrightsideSession:
    def __init__(self, host_id, grid_url, metadata={}) -> None:
        """
        Data class for a Brightside session
        """

        self._host_id = host_id
        self._grid_url = grid_url
        self._metadata = metadata

    @property
    def host_id(self) -> str:
        """
        The ID of the Brightside session
        """
        return self._host_id

    @property
    def grid_url(self) -> str:
        """
        The URL of the Selenium Grid hub
        """
        return self._grid_url

    @property
    def metadata(self) -> dict:
        """
        Metadata of the Brightside session
        """
        return self._metadata
