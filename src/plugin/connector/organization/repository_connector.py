from .. import RequestConnector
import logging


class OrgRepositoryConnector(RequestConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_repositories(self, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/orgs/{secret_data.get('org_name')}/repos"
        response = self.send_request(url, headers, page=1)
        return response
