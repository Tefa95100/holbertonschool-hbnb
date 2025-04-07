from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

owner_model = api.model('PlaceOwner', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})


# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(
        required=True,
        description='Title of the place'),
    'description': fields.String(
        description='Description of the place',
        ),
    'price': fields.Float(
        required=True,
        description='Price per night',
        min=0,
        ),
    'latitude': fields.Float(
        required=True,
        description='Latitude of the place',
        min=-90,
        max=90,
        ),
    'longitude': fields.Float(
        required=True,
        description='Longitude of the place',
        min=-180,
        max=180,
        ),
    'owner': fields.String(
        required=True,
        description='ID of the owner'
        ),
    'amenities': fields.List(
        fields.String,
        required=False,
        description="List of amenities ID's"
        )
})

# Special model when updating a place
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(
        required=True,
        description='Title of the place'),
    'description': fields.String(
        description='Description of the place',
        ),
    'price': fields.Float(
        required=True,
        description='Price per night',
        min=0,
        )
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        # Check if user UUID exist
        owners = facade.get_all_users()
        for owners_item in owners:
            if owners_item.id == place_data['owner']:
                break
        else:
            return {'message': 'The given owner UUID does not exist'}, 400

        # Convert price to 2 digit :
        place_data['price'] = round(place_data['price'], 2)

        place = facade.create_place(place_data)
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': place.owner,
            'amenities': place.amenities,
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': place.owner,
            'amenities': place.amenities
        } for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if place:
            # Fetch owner details using the owner ID
            owner_id = place.owner
            owner = None

            # Find the owner in the list of users
            users = facade.get_all_users()
            for user in users:
                if user.id == owner_id:
                    owner = user
                    break

            # Prepare owner data
            owner_data = {
                'id': owner_id,
                'first_name': owner.first_name if owner else (
                    "Owner first name"),
                'last_name': owner.last_name if owner else (
                    "Owner last name"),
                'email': owner.email if owner else "Owner email"
            }

            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': owner_data,
                'amenities': place.amenities
                }, 200
        return {'message': 'Place not found'}, 404

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload

        if not place_data:
            return {'message': 'No data provided'}, 400

        # Check if user UUID exist
        if "owner" in place_data:
            owners = facade.get_all_users()
            for owners_item in owners:
                if owners_item.id == place_data['owner']:
                    break
            else:
                return {'message': 'The given owner UUID does not exist'}, 400

        # Convert price to 2 digit :
        if "price" in place_data:
            place_data['price'] = round(place_data['price'], 2)

        place = facade.update_place(place_id, place_data)
        if place:
            return {'message': 'Place updated successfully'}, 200
        return {'message': 'Place not found'}, 404
