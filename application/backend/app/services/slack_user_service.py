from app.models.slack_user import SlackUser
from app.models.slack_user_schema import SlackUserSchema

class SlackUserService:
    def get(self, filters, page, per_page, order_by_ascending = True):
        order_by = SlackUser.current_username.asc if order_by_ascending else SlackUser.current_username.desc
        return SlackUser.get(filters = filters, page = page, per_page = per_page, order_by = order_by)

    def get_by_id(self, slack_user_id):
        return SlackUser.get_by_id(slack_user_id)

    def add(self, data):
        return SlackUser.upsert(data)

    def update(self, slack_user_id, data):
        slack_user = SlackUser.get_by_id(slack_user_id)

        if slack_user is None:
            return None

        updated_slack_user = SlackUserSchema().load(data=data, instance=slack_user, partial=True)
        return SlackUser.upsert(updated_slack_user)

    def get_user_ids_to_invite(self, number_to_invite, event_id, number_of_user, people_per_event):
        users_to_invite = SlackUser.get_users_to_invite(number_to_invite, event_id, number_of_user, people_per_event)
        return [user[0] for user in users_to_invite]
