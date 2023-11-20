import abc
import requests
import logging

from plugin.connector import RequestConnector

_LOGGER = logging.getLogger(__name__)


class DockerhubConnector(RequestConnector):

    def list_tags(self, namespace, repository, secret_data):
        url = f'https://hub.docker.com/v2/namespaces/{namespace}/repositories/{repository}/tags'
        headers = self.make_header_dockerhub(secret_data)

        try:
            response = self.send_request(url, headers=headers)
            _response = list(response)
            if _response and _response[0].get('results'):
                results = _response[0].get('results')

                return results
            else:
                return []
        except Exception as e:
            _LOGGER.error(f"Request Error: {e}")
            raise e
