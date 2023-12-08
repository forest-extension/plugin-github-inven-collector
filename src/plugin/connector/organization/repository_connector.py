from .. import RequestConnector
import logging


class OrgRepositoryConnector(RequestConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_repositories(self, secret_data):
        headers = self.make_header(secret_data)
        url = (
            f"https://api.github.com/orgs/{secret_data.get('organization_name')}/repos"
        )
        response = self.send_request(url, headers, page=1)
        return response

    def list_repository_issues(self, repo, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/repos/{secret_data.get('organization_name')}/{repo}/issues"
        response = self.send_request(url, headers, page=1)
        return response

    def get_repository_languages(self, repo, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/repos/{secret_data.get('organization_name')}/{repo}/languages"
        response = self.send_request(url, headers)
        return response

    def get_repository_contributors(self, repo, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/repos/{secret_data.get('organization_name')}/{repo}/contributors"
        response = self.send_request(url, headers)
        return response

    def list_repository_branches(self, repo, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/repos/{secret_data.get('organization_name')}/{repo}/branches"
        response = self.send_request(url, headers, page=1)
        return response

    def list_repository_forks(self, repo, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/repos/{secret_data.get('organization_name')}/{repo}/forks"
        response = self.send_request(url, headers, page=1)
        return response

    def get_user(self, user, secret_data):
        headers = self.make_header(secret_data)
        url = f"https://api.github.com/users/{user}"
        response = self.send_request(url, headers)
        return response
