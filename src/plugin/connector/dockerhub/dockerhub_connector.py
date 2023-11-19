import abc
import requests
import logging

_LOGGER = logging.getLogger(__name__)

from spaceone.core.connector import BaseConnector


class RegistryConnector(BaseConnector):

    @abc.abstractmethod
    def get_tags(self, registry_url, image):
        pass


class DockerHubConnector(RegistryConnector):
    def get_tags(self, namespace, repository):
        url = f'https://hub.docker.com/v2/{namespace}/{repository}/tags'

        response = requests.get(url)

        if response.status_code == 200:
            results = response.json().get('results', [])
            return results

        else:
            # raise ERROR_NO_IMAGE_IN_REGISTRY(registry_type='DOCKER_HUB', image=image)
            print(f'[ERROR] {response.status_code} {response.text}')
