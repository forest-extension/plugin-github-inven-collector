import logging
import requests

from spaceone.core.connector import BaseConnector


_LOGGER = logging.getLogger(__name__)


class RepositoryConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_organization_repos(self, url, secret_data):
        headers = self.create_headers(secret_data)
        try:
            response = requests.get(url, headers=headers).json()
            return response
        except Exception as e:
            _LOGGER.error(f"Request Error: {e}")
            raise e

    def list_repo_tags(self, url, secret_data):
        headers = self.create_headers(secret_data)
        try:
            response = requests.get(url, headers=headers).json()
            return response
        except Exception as e:
            _LOGGER.error(f"Request Error: {e}")
            raise e

    @staticmethod
    def create_headers(secret_data):
        github_token = secret_data.get("github_token")
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        return headers
