from app.models.restaurant import Restaurant
from app.models.restaurant_schema import RestaurantSchema

class RestaurantService:
    def get(self, filters, page, per_page):
        return Restaurant.get(filters = filters, page = page, per_page = per_page)

    def get_by_id(self, restaurant_id):
        return Restaurant.get_by_id(restaurant_id)

    def add(self, data):
        return Restaurant.upsert(data)

    def update(self, restaurant_id, data):
        restaurant = Restaurant.get_by_id(restaurant_id)

        if restaurant is None:
            return None

        updated_restaurant = RestaurantSchema().load(data=data, instance=restaurant, partial=True)
        return Restaurant.upsert(updated_restaurant)

    def delete(self, restaurant_id):
        restaurant = Restaurant.get_by_id(restaurant_id)
        if restaurant is not None:
            updated_restaurant = RestaurantSchema().load(data={"deleted": True}, instance=restaurant, partial=True)
            Restaurant.upsert(updated_restaurant)
