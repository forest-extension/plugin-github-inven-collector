import logging

from spaceone.inventory.plugin.collector.lib import *
from ..connector.repo_connector import RepoConnector


_LOGGER = logging.getLogger("cloudforet")


class RepoManager:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Repository"
        self.cloud_service_type = "Issue"
        self.provider = "Github"
        self.metadata_path = "plugin/metadata/repository/issues.yaml"

    def collect_resources(self, options, secret_data, schema):
        try:
            yield from self.collect_cloud_service_type(options, secret_data, schema)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
                resource_type="inventory.CloudServiceType",
            )

        try:
            yield from self.collect_cloud_service(options, secret_data, schema)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self, options, secret_data, schema):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
        )

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "reference.resource_id", "account", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, options, secret_data, schema):
        repo_connector = RepoConnector()
        repos = repo_connector.get_repositories(secret_data)

        all_issues = []

        _LOGGER.debug(f"Repos: {repos}")

        for repo in repos:
            _LOGGER.debug(f"Processing repo: {repo}")

            owner = repo.get("owner", {})
            repo_name = repo.get("name")

            if repo_name and owner:
                repo_owner = owner.get("login")

                _LOGGER.debug(f"Processing issues for repo: {repo_name}")

                issues = repo_connector.get_repo_issues(secret_data, repo_owner, repo_name)
                pulls = repo_connector.get_repo_pulls(secret_data, repo_owner, repo_name)

                for issue in issues:
                    issue["repo_name"] = repo_name
                    issue["pulls"] = pulls

                all_issues.extend(issues)
            else:
                _LOGGER.warning("Missing required attributes in repo: {repo}")

        all_issues.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        for issue in all_issues:
            labels = issue.get("labels", [])
            issue_labels = {label.get("name"): label for label in labels}
            issue["labels"] = issue_labels

            cloud_service = make_cloud_service(
                name=self.cloud_service_type,
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=issue,
            )

            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )

