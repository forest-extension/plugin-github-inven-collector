import abc
import requests
import logging

from spaceone.core.connector import BaseConnector

_LOGGER = logging.getLogger(__name__)


class RegistryConnector(BaseConnector):

    @abc.abstractmethod
    def get_tags(self, registry_url, image):
        pass


class DockerhubConnector(RegistryConnector):
    def get_tags(self, namespace, repository):
        url = f'https://hub.docker.com/v2/namespaces/{namespace}/repositories/{repository}/tags'

        response = requests.get(url)

        if response.status_code == 200:
            results = response.json().get('results', [])
            return results

        else:
            # raise ERROR_NO_IMAGE_IN_REGISTRY(registry_type='DOCKER_HUB', image=image)
            print(f'[ERROR] {response.status_code} {response.text}')
            return []
