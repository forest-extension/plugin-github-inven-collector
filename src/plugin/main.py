from spaceone.inventory.plugin.collector.lib.server import CollectorPluginServer

from .manager.org_manager import OrgManager
from .manager.repository_manager import RepositoryManager
from .manager import GithubBaseManager

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

    secret_data = params["secret_data"]
    options = params["options"]
    repo_manager = RepositoryManager()

    return repo_manager.collect_resources(options, secret_data, schema="")
