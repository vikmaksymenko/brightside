from abc import ABC, abstractmethod

from sessions.brightsideSession import BrightsideSession


class AbstractSessionManager(ABC):
    @abstractmethod
    def setup_host(self, request) -> BrightsideSession:
        """
        Prepares a host

          :param request: The request object from the Flask app
          :type request: Flask request object
          :return: The Brightside session
        """
        pass

    @abstractmethod
    def terminate_host(self, host_id) -> None:
        """
        Deletes the session

            :param host_id: The session ID of the session to delete
            :type host_id: string
            :return: None

        """
        pass

    @abstractmethod
    def find_host(self, host_id) -> BrightsideSession:
        """
        Find a host by host ID and return it's info
            :param host_id: The session ID of the session to find
            :type host_id: string
            :return: The Brightside session
        """
        pass
