import logging
from spaceone.inventory.plugin.collector.lib import *

from ...connector.organization.repository_connector import OrgRepositoryConnector

_LOGGER = logging.getLogger("cloudforet")


class OrgRepositoryManager:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Organization"
        self.cloud_service_type = "Repository"
        self.provider = "github_wanjin"
        self.metadata_path = "metadata/organization/repository.yaml"

    def collect_resources(self, options, secret_data, schema):
        try:
            yield from self.collect_cloud_service_type(options, secret_data, schema)
            yield from self.collect_cloud_service(options, secret_data, schema)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self, options, secret_data, schema):
        try:
            cloud_service_type = make_cloud_service_type(
                name=self.cloud_service_type,
                group=self.cloud_service_group,
                provider=self.provider,
                metadata_path=self.metadata_path,
                is_primary=True,
                is_major=True,
                tags={
                    "spaceone:icon": "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png"
                },
            )

            yield make_response(
                cloud_service_type=cloud_service_type,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
                resource_type="inventory.CloudServiceType",
            )

        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service(self, options, secret_data, schema):
        try:
            org_repository_connector = OrgRepositoryConnector()
            repo_items = org_repository_connector.list_repositories(secret_data)
            for item in repo_items:
                # get issues
                issue_items = org_repository_connector.list_repository_issues(
                    item["name"], secret_data
                )
                item["issues"] = list(issue_items)

                # get languages
                (language_info,) = org_repository_connector.get_repository_languages(
                    item["name"], secret_data
                )
                languages = []
                for key, value in language_info.items():
                    languages.append({"language": key, "bytes": value})
                item["languages"] = languages

                # get contributors
                (
                    contributor_items,
                ) = org_repository_connector.get_repository_contributors(
                    item["name"], secret_data
                )
                contributors_info = []
                # get contributors info
                for contributor_item in contributor_items:
                    (contributor_info,) = org_repository_connector.get_user(
                        contributor_item["login"], secret_data
                    )
                    contributor_info["contributions"] = contributor_item["contributions"]
                    contributors_info.append(contributor_info)
                item["contributors"] = contributors_info

                # get branches
                branch_items = org_repository_connector.list_repository_branches(
                    item["name"], secret_data
                )
                item["branches"] = list(branch_items)

                # get forks
                fork_items = org_repository_connector.list_repository_forks(
                    item["name"], secret_data
                )
                forks_info = []
                # get forked repo owners info
                for fork_item in fork_items:
                    (owner_info,) = org_repository_connector.get_user(
                        fork_item["owner"]["login"], secret_data
                    )
                    forks_info.append(
                        {
                            "name": fork_item["name"],
                            "description": fork_item["description"],
                            "html_url": fork_item["html_url"],
                            "open_issues_count": fork_item["open_issues_count"],
                            "forks_count": fork_item["forks_count"],
                            "owner_info": owner_info,
                        }
                    )
                item["forks_info"] = forks_info

                cloud_service = make_cloud_service(
                    name=item["name"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=item,
                )

                yield make_response(
                    cloud_service=cloud_service,
                    match_keys=[
                        ["name", "reference.resource_id", "account", "provider"]
                    ],
                )
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )
