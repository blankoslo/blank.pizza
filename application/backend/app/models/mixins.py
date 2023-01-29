from copy import deepcopy
from app.models import db
from sqlalchemy import desc, asc
import enum

def get_field(schema, field):
    field = deepcopy(schema._declared_fields[field.key])
    field.required = False
    return field

class CrudMixin(object):
    @classmethod
    def get(cls, filters, order_by = None, page = None, per_page = None, session=db.session):
        query = cls.query
        # Add filters to the query
        for attr, value in filters.items():
            query = query.filter(getattr(cls, attr) == value)
        # Add order by to the query
        if (order_by):
            query = query.order_by(order_by())
        # If pagination is on, paginate the query
        if (page and per_page):
            pagination = query.paginate(page, per_page, False)
            return pagination.total, pagination.items
            
        res = query.count(), query.all()
        return res

    @classmethod
    def get_like(cls, filters, order_by = None, page = None, per_page = None, session=db.session):
        query = cls.query
        # Add filters to the query
        for attr, value in filters.items():
            query = query.filter(getattr(cls, attr).like("%%%s%%" % value))
        # Add order by to the query
        if (order_by):
            query = query.order_by(order_by())
        # If pagination is on, paginate the query
        if (page and per_page):
            pagination = query.paginate(page, per_page, False)
            return pagination.total, pagination.items
            
        res = query.count(), query.all()
        return res
    
    @classmethod
    def get_by_filter(cls, filters, session=db.session):
        query = cls.query
        for attr, value in filters.items():
            query = query.filter(getattr(cls, attr) == value)
        return query.all()

    @classmethod
    def get_by_id(cls, id, session=db.session):
        return cls.query.get(id)
    
    @classmethod
    def delete(cls, id, session=db.session):
        obj = cls.query.get(id)
        if obj != None:
            session.delete(obj)
            session.commit()
    
    @classmethod
    def upsert(cls, schema, session=db.session):
        session.add(schema)
        session.commit()
    
    @classmethod
    def count(cls, session=db.session):
        return cls.query.count()
