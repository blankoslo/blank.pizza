from flask import views
from flask_smorest import Blueprint, abort
from app.models.restaurant import Restaurant, RestaurantSchema, RestaurantQueryArgsSchema, RestaurantUpdateSchema
from flask_jwt_extended import jwt_required

bp = Blueprint("restaurants", "restaurants", url_prefix="/restaurants", description="Operations on restaurants")

@bp.route("/")
class Restaurants(views.MethodView):
    @bp.arguments(RestaurantQueryArgsSchema, location="query")
    @bp.response(200, RestaurantSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List restaurants"""
        total, restaurants = Restaurant.get(filters = args, page = pagination_parameters.page, per_page = pagination_parameters.page_size)
        print(restaurants[0].ratings)
        print(restaurants[0].rating)
        pagination_parameters.item_count = total
        return restaurants
    
    @bp.arguments(RestaurantSchema)
    @bp.response(201, RestaurantSchema)
    @jwt_required()
    def post(self, new_data):
        """Add an restaurant"""
        Restaurant.upsert(new_data)
        return new_data

@bp.route("/<restaurant_id>")
class RestaurantsById(views.MethodView):
    @bp.response(200, RestaurantSchema)
    def get(self, restaurant_id):
        """Get restaurant by ID"""
        restaurant = Restaurant.get_by_id(restaurant_id)
        if restaurant == None:
            abort(404, message = "Restaurant not found.")
        return restaurant
    
    @bp.arguments(RestaurantUpdateSchema)
    @bp.response(200, RestaurantSchema)
    @jwt_required()
    def put(self, update_data, restaurant_id):
        """Update existing restaurant"""
        restaurant = Restaurant.get_by_id(restaurant_id)
        if restaurant == None:
            abort(422, message = "Restaurant not found.")
        updated_restaurant = RestaurantSchema().load(data=update_data, instance=restaurant, partial=True)
        Restaurant.upsert(updated_restaurant)
        return updated_restaurant

    @bp.response(204)
    @jwt_required()
    def delete(self, restaurant_id):
        """Delete restaurant"""
        restaurant = Restaurant.get_by_id(restaurant_id)
        if restaurant == None:
            abort(422, message = "Restaurant not found.")
        updated_restaurant = RestaurantSchema().load(data={"deleted": True}, instance=restaurant, partial=True)
        Restaurant.upsert(updated_restaurant)