import logging

from spaceone.inventory.plugin.collector.lib.server import CollectorPluginServer
from plugin.manager.repository_manager import RepositoryManager

_LOGGER = logging.getLogger('cloudforet')

app = CollectorPluginServer()


@app.route('Collector.init')
def collector_init(params: dict) -> dict:
    return {'metadata': {'options_schema': _create_options_schema()}}


@app.route('Collector.collect')
def collector_collect(params: dict) -> dict:
    options = params['options']
    secret_data = params['secret_data']
    schema = params.get('schema')

    repository_manager = RepositoryManager()
    return repository_manager.collect_resources(options, secret_data, schema)


def _create_options_schema():
    return {
        'required': ['items'],
        'order': ['items'],
        'type': 'object',
        'properties': {
            'items': {
                'title': 'Item filter',
                'type': 'array',
                'items': {
                    'enum': [
                        'fields'
                    ]
                }
            }
        }
    }
