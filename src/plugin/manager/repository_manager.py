import logging
from spaceone.inventory.plugin.collector.lib import *
from packaging import version
from plugin.connector.repository_connector import RepositoryConnector
from plugin.connector.dockerhub.dockerhub_connector import DockerhubConnector

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
            repo_name = item.get('name')
            item['github_tag'] = self.get_latest_tag(repo_name, secret_data)
            item['dev_dockerhub_tag'] = self.get_latest_dockerhub_tag(
                secret_data['dev_dockerhub'], item.name, secret_data
            )
            item['prod_dockerhub_tag'] = self.get_latest_dockerhub_tag(
                secret_data['prod_dockerhub'], item.name, secret_data
            )
            item['pypi_tag'] = self.get_latest_pypi_tag(item['name'], secret_data)
            item['type'] = self.get_repo_type_by_topics(item['topics'])
            item['topics'] = item.topics
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
        all_tag_items = []
        page = 1
        repository_connector = RepositoryConnector()

        while True:
            tag_items = repository_connector.list_repo_tags(repo_name, secret_data, page)
            print(len(tag_items))
            if not tag_items:
                break

            all_tag_items.extend(tag_items)
            page += 1

        versions = [version.parse(item['name']) for item in all_tag_items]
        latest_version = max(versions)
        return str(latest_version)

    @staticmethod
    def get_latest_dockerhub_tag(namespace, repo_name, secret_data) -> str:
        dockerhub_connector = DockerhubConnector()
        tag_items = dockerhub_connector.get_tags(namespace, repo_name)

        tag_items.sort(key=lambda x: x['last_updated'], reverse=True)

        return tag_items[0].name

    @staticmethod
    def get_latest_pypi_tag(repo_name, secret_data) -> str:
        return '1.0.0'

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
