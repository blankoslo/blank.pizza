from logging import Logger
from typing import Optional
import json

from src.broker.broker_client import BrokerClient
from src.injector import injector
from src.slack.lmdb import LMDB

from slack_sdk.oauth.installation_store.installation_store import InstallationStore
from slack_sdk.oauth.installation_store.models.installation import Installation


class BrokerInstallationStore(InstallationStore):
    def __init__(self):
        self.storage = LMDB("slack_installations")

    def save(self, installation: Installation):
        print("Tried to save an installation through the bot. NOT SUPPORTED")
        pass

    def find_installation(
            self,
            *,
            enterprise_id: Optional[str],
            team_id: Optional[str],
            user_id: Optional[str] = None,
            is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        if is_enterprise_install or team_id is None:
            print("Enterprise is true or team_id is None")
            return None

        # Try to get installation from cache
        installation = self.storage.get(team_id)
        if installation is None:
            # Get installation from Backend through Broker
            client = injector.get(BrokerClient)
            installation = client.get_slack_installation(team_id)
            # Cache installation
            self.storage.put(team_id, json.dumps(installation))
            # Close connection
            client.disconnect()
        else:
            # Parse installation json
            installation = json.loads(installation)

        # If installation doesnt exist then log and return None
        if installation is None:
            print("Unable to find installation")
            return None

        return Installation(
            app_id=installation['app_id'],
            enterprise_id=installation.get('enterprise_id'),
            enterprise_name=installation.get('enterprise_name'),
            team_id=installation['team_id'],
            team_name=installation.get('team_name'),
            bot_token=installation['access_token'],
            bot_user_id=installation['bot_user_id'],
            enterprise_url=None,
            bot_id=None,
            bot_scopes=None,
            bot_refresh_token=None,
            bot_token_expires_at=None,
            user_id=None,
            user_token=None,
            user_scopes=None,
            user_refresh_token=None,
            user_token_expires_at=None,
            incoming_webhook_url=None,
            incoming_webhook_channel=None,
            incoming_webhook_channel_id=None,
            incoming_webhook_configuration_url=None,
            is_enterprise_install=None,
            token_type=None,
            installed_at=None,
        )

    def delete_bot(
            self,
            *,
            enterprise_id: Optional[str],
            team_id: Optional[str],
    ) -> None:
        """Deletes a bot scope installation per workspace / org"""
        self._delete_workspace(team_id=team_id, enterprise_id=enterprise_id)

    def delete_installation(
            self,
            *,
            enterprise_id: Optional[str],
            team_id: Optional[str],
            user_id: Optional[str] = None,
    ) -> None:
        """Deletes an installation that matches the given IDs"""
        self._delete_workspace(team_id=team_id, enterprise_id=enterprise_id)

    def _delete_workspace(self, team_id, enterprise_id):
        print("Deleting workspace with team_id %s and enterprise_id %s" % (team_id, enterprise_id))
        client = injector.get(BrokerClient)
        client.deleted_slack_organization_event(team_id=team_id, enterprise_id=enterprise_id)
        client.disconnect()
        self.storage.delete(team_id)


