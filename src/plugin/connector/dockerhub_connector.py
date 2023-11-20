import abc
import requests
import logging

from plugin.connector import RequestConnector

_LOGGER = logging.getLogger(__name__)


class DockerhubConnector(RequestConnector):

    def list_tags(self, namespace, repository, secret_data):
        url = f'https://hub.docker.com/v2/namespaces/{namespace}/repositories/{repository}/tags'
        headers = self.make_header(secret_data)

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json().get('results', [])
            return results

        else:
            # raise ERROR_NO_IMAGE_IN_REGISTRY(registry_type='DOCKER_HUB', image=image)
            print(f'[ERROR] {response.status_code} {response.text}')
            return []
