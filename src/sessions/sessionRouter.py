import logging
import requests

from .sessionManagerFactory import SessionManagerFactory
from ..utils.selenium_grid_utils import GridHelper

class SessionRouter:
    def __init__(self, platform):
        """
        Initialize the session router with the platform to use.
        Session router is responsible for creating, deleting and proxying requests to the browser sessions

            :param platform: The platform to use (Selenium Grid, Kubernetes, Docker, etc.)
            :type platform: string
        """

        self._session_manager = SessionManagerFactory.platformFor(platform)
        self._sessions = {}

    def create_session(self, request):
        """
        Create a session in the platform and add it to the sessions dictionary
        As a key, use the Brightside session ID.
        The Brightside session ID is the combination of the host ID (container or pod) and the selenium session ID
        In the response, replace the Selenium session ID with the Brightside session ID

            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: The response from the Selenium Grid hub with modified session ID
        """
        brightside_session = self._session_manager.setup_host(request)

        GridHelper.wait_for_grid_4_availability(brightside_session.grid_url)

        logging.info(f"Starting Selenium session on {brightside_session.host_id}")   
        response = self._api_request(brightside_session.grid_url + "/session", request)
        # TODO: Handle error response

        browser_session_id = response["value"]["sessionId"]
        logging.info(f"Started Selenium session {browser_session_id} on {brightside_session.host_id}")

        brightside_id = brightside_session.host_id + browser_session_id
        self._sessions[brightside_id] = brightside_session
        response["value"]["sessionId"] = brightside_id

        return response

    def proxy_requests(self, session_id, path, request):
        """
        Proxy requests to the browser session in the platform

            :param session_id: The Brightside session ID of the session to proxy the request to
            :type session_id: string
            :param path: The path to proxy the request to
            :type path: string
            :param request: The request object from the Flask app
            :type request: Flask request object
            :return: The response from the Selenium Grid hub
        """

        host_id, browser_session_id = self._parse_brightside_id(session_id)

        if session_id in self._sessions:
            session = self._sessions[session_id]
        else:
            session = self._session_manager.find_host(host_id)

        if session is None:
            raise Exception(f"Session {session_id} not found")
        
        url = f"{session.grid_url}/session/{browser_session_id}/{path}"
        logging.info(f"Forwarding request to {url}")
        
        return self._api_request(url,request)

    def delete_session(self, session_id, request):
        """
        Deletes the session in the platform and removes it from the sessions dictionary

            :param session_id: The Brightside session ID of the session to delete
            :type session_id: string
            :return: The response from the Selenium Grid hub
        """
        host_id, _ = self._parse_brightside_id(session_id)
        self._session_manager.terminate_host(host_id)
        return GridHelper.empty_response

    def _cleanup_sessions_list(self):
        """
        Remove sessions from the sessions dictionary that are not present in the session manager
        Runs on schedule in separate thread
        """

        pass

    def _api_request(self, url, request):
        return requests.request(
            request.method, url, data=request.data, headers=request.headers
        ).json()

    def _parse_brightside_id(self, brightside_id):
        """
        Parse the Brightside session ID into the host ID and the Selenium session ID

            :param brightside_id: The Brightside session ID to parse
            :type brightside_id: string
            :return: The host ID and the Selenium session ID
        """
        return brightside_id[:-32], brightside_id[-32:]
