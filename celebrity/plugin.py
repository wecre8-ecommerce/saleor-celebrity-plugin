from saleor.graphql.views import GraphQLView

from saleor.plugins.base_plugin import BasePlugin
from celebrity.graphql.schema import schema


class CelebrityPlugin(BasePlugin):
    name = "celebrity"
    DEFAULT_ACTIVE = True
    PLUGIN_ID = "celebrity"
    PLUGIN_NAME = "celebrity"
    CONFIGURATION_PER_CHANNEL = False

    def webhook(self, request, path, previous_value):
        view = GraphQLView.as_view(schema=schema)
        request.app = self
        return view(request)
