import requests
from ..connector import RequestConnector


class OrgConnector(RequestConnector):
    def __init__(self):
        super().__init__()

    def get_org(self, secret_data):
        org_name = secret_data.get("org_name")
        url = f"https://api.github.com/orgs/{org_name}"
        headers = self.make_header(secret_data)

        return self.send_request(url, headers)

    def get_org_repos(self, secret_data):
        org_name = secret_data.get("org_name")
        url = f"https://api.github.com/orgs/{org_name}/repos"
        headers = self.make_header(secret_data)
        return self.send_request(url, headers, page=1, per_page=1)
