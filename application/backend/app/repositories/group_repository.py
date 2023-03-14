from app.models.group import Group
from app.models.mixins import CrudMixin
from app.db import db

class GroupRepository(Group, CrudMixin):
    @classmethod
    def get(cls, filters=None, order_by=None, page=None, per_page=None, team_id=None, session=db.session):
        query = cls.query

        if team_id:
            query = query.filter(Group.slack_organization_id == team_id)

        if filters is None:
            filters = {}
        # Add filters to the query
        for attr, value in filters.items():
            query = query.filter(getattr(cls, attr) == value)
        # Add order by to the query
        if (order_by):
            query = query.order_by(order_by())
        # If pagination is on, paginate the query
        if (page and per_page):
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            return pagination.total, pagination.items

        res = query.count(), query.all()
        return res
