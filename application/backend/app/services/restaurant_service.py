from app.models.restaurant import Restaurant

class RestaurantService:
    def get_by_id(self, restaurant_id):
        return Restaurant.get_by_id(restaurant_id)
