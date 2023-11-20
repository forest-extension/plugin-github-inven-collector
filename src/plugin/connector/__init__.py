import logging
from spaceone.core.connector import BaseConnector
import requests

__all__ = ["GitHubConnector"]

_LOGGER = logging.getLogger(__name__)

class GitHubConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def send_request(url, headers, params=None, method="GET", page=None, per_page=30):
        try:
            if page:
                for response in GitHubConnector._pagination(url, headers, params, per_page, page):
                    yield response
            else:
                response = GitHubConnector._make_request(url, headers, params, method)
                yield response
        except Exception as e:
            _LOGGER.error(f"Request Error: {e}")
            raise e

    @staticmethod
    def _make_request(url, headers, params=None, method="GET"):
        response = None
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)

            response.raise_for_status()
            response_json = response.json()

            return response_json
        except requests.exceptions.HTTPError as errh:
            _LOGGER.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            _LOGGER.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            _LOGGER.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            _LOGGER.error(f"Request Error: {err}")

        if response and not response.content:
            _LOGGER.warning(f"Non-JSON response received: {response.content}")

        return None

    @staticmethod
    def _pagination(url, headers, params, per_page, page):
        responses = []
        while True:
            paginated_url = f"{url}{'&' if '&' in url else '?'}per_page={per_page}&page={page}"
            response_json = GitHubConnector._make_request(paginated_url, headers, params)

            if not response_json:
                break

            page += 1
            responses.extend(response_json)

        return responses

    @staticmethod
    def make_header(secret_data):
        github_token = secret_data.get("github_token")
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
