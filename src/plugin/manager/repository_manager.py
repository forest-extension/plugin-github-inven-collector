import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.connector.repository_connector import RepositoryConnector

_LOGGER = logging.getLogger(__name__)


class RepositoryManager:
    def __init__(self, **kwargs):
        self.connector: RepositoryConnector = RepositoryConnector(**kwargs)

        self.cloud_service_group = 'Repository'
        self.cloud_service_type = 'Repository'
        self.provider = 'github'
        self.metadata_path = 'plugin/metadata/repository/repository.yaml'

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
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True
        )

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[['name', 'reference.resource_id', 'account', 'provider']],
            resource_type='inventory.CloudServiceType'
        )

    def collect_cloud_service(self, options, secret_data, schema):
        repository_connector = RepositoryConnector()
        repo_items = repository_connector.list_organization_repos(secret_data)
        for item in repo_items:
            item['github_tag'] = self.get_latest_tag(item.name, secret_data)
            item['dev_dockerhub_tag'] = '1.0.0'
            item['prod_dockerhub_tag'] = '1.0.0'
            item['pypi_tag'] = '1.0.0'
            item['type'] = self.get_repo_type_by_topics(item.topics)
            cloud_service = make_cloud_service(
                name=self.cloud_service_type,
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=item,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )

    @staticmethod
    def get_latest_tag(repo_name, secret_data) -> str:
        repository_connector = RepositoryConnector()
        tag_items = repository_connector.list_repo_tags(repo_name, secret_data)

        for item in tag_items:
            tag_commit_sha = item.commit.sha
            commit_by_sha = repository_connector.get_commit_by_sha(repo_name, tag_commit_sha, secret_data)
            tag_items['date'] = commit_by_sha.committer.data

        tag_items.sort(key=lambda x: x['date'], reverse=True)

        return tag_items[0].name

    @staticmethod
    def get_repo_type_by_topics(topics: list):
        if 'plugin' in topics:
            return 'plugin'
        elif 'core' in topics:
            return 'core'
        elif 'doc' in topics:
            return 'doc'
        elif 'spacectl' in topics:
            return 'tools'
        else:
            return 'common'