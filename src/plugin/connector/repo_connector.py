from . import GitHubConnector


class RepoConnector(GitHubConnector):

    def get_repositories(self, secret_data):
        org_name = secret_data.get("org_name")
        url = f"https://api.github.com/orgs/{org_name}/repos"
        headers = self.make_header(secret_data)
        return self.send_request(url, headers, page=1000)

    def get_repo_issues(self, secret_data, repo_owner, repo_name):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
        headers = self.make_header(secret_data)
        return self.send_request(url, headers, page=1000)

    def get_repo_pulls(self, secret_data, repo_owner, repo_name):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
        headers = self.make_header(secret_data)
        return self.send_request(url, headers, page=1000)
