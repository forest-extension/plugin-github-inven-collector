import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *

from plugin.connector.repository_connector import RepositoryConnector

_LOGGER = logging.getLogger(__name__)


class RepositoryManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = 'Repository'
        self.cloud_service_type = 'Repository'
        self.provider = 'github'
        self.metadata_path = 'plugin/metadata/repository/repository.yaml'

        self.organization = 'cloudforet-io'
        self.base_url = 'https://api.github.com'

    def collect_resources(self, options, secret_data, schema):
        try:
            # yield from self.collect_cloud_service_type(options, secret_data, schema)
            yield from self.collect_cloud_service(options, secret_data, schema)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service(self, options, secret_data, schema):
        repos_url = f'{self.base_url}/orgs/{self.organization}/repos'
        repository_connector = RepositoryConnector(secret_data)
        repository_items = repository_connector.get_organization_repos(repos_url, secret_data)

        for item in repository_items:
            tags_url = f'{self.base_url}/repos/{self.organization}/{item["name"]}/tags'
            tag_items = repository_connector.get_repo_tags(tags_url, secret_data)
            item['tags'] = tag_items

            cloud_service = make_cloud_service(
                name=self.cloud_service_type,
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=item
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[['name', 'reference.resource_id', 'account', 'provider']]
            )