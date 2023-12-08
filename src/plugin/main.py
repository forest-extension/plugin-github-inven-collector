import logging

from spaceone.inventory.plugin.collector.lib.server import CollectorPluginServer
from plugin.manager.organization.repository_manager import OrgRepositoryManager

_LOGGER = logging.getLogger("cloudforet")

app = CollectorPluginServer()


@app.route("Collector.init")
def collector_init(params: dict) -> dict:
    """init plugin by options

    Args:
        params (CollectorInitRequest): {
            'options': 'dict',    # Required
            'domain_id': 'str'
        }

    Returns:
        PluginResponse: {
            'metadata': 'dict'
        }
    """

    return {"metadata": {}}


@app.route("Collector.collect")
def collector_collect(params: dict) -> dict:
    """Collect external data

    Args:
        params (CollectorCollectRequest): {
            'options': 'dict',      # Required
            'secret_data': 'dict',  # Required
            'schema': 'str',
            'domain_id': 'str'
        }

    Returns:
        Generator[ResourceResponse, None, None]
        {
            'state': 'SUCCESS | FAILURE',
            'resource_type': 'inventory.CloudService | inventory.CloudServiceType | inventory.Region',
            'resource_data': 'dict',
            'match_keys': 'list',
            'error_message': 'str'
            'metadata': 'dict'
        }
    """

    options = params["options"]
    secret_data = params["secret_data"]
    schema = params.get("schema")

    org_repository_manager = OrgRepositoryManager()
    # return org_repository_manager.collect_cloud_service_type(options, secret_data, schema)
    return org_repository_manager.collect_resources(options, secret_data, schema)
