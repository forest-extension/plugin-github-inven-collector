import logging
import requests

from plugin.connector import RequestConnector

_LOGGER = logging.getLogger(__name__)


class RepositoryConnector(RequestConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_organization_repos(self, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/orgs/{secret_data.get('org_name')}/repos"
        try:
            response = self.send_request(url, headers=headers).json()
            return response
        except Exception as e:
            _LOGGER.error(f"Request Error: {e}")
            raise e

    def list_repo_tags(self, repo_name, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/repos/{secret_data.get('org_name')}/{repo_name}/tags"
        try:
            response = self.send_request(url, headers=headers, per_page=9999).json()
            return response
        except Exception as e:
            _LOGGER.error(f"Request Error: {e}")
            raise e

    def get_commit_by_sha(self, repo_name, sha, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/repos/{secret_data.get('org_name')}/{repo_name}/git/commits/{sha}"
        try:
            response = self.send_request(url, headers=headers).json()
            return response
        except Exception as e:
            _LOGGER.error(f"Request Error: {e}")
            raise e

    def list_repo_topics(self, repo_name, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/repos/{secret_data.get('org_name')}/{repo_name}/topics"
        try:
            response = self.send_request(url, headers=headers).json()
            return response
        except Exception as e:
            _LOGGER.error(f"Request Error: {e}")
            raise e
