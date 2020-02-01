"""
app.api.farms
~~~~~~~~~~~~~~~~~

"""

from flask_restful import Resource, reqparse, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app.models import Farm
from app import db
from .common.errors import raise_error
from .common.utils import (
    valid_farm_name, valid_location, valid_description, valid_units,
    valid_active_status, valid_margin, valid_farm_stage, valid_location, 
    valid_date, valid_price
)
from app.decorators import admin_required

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('location', type=str)
parser.add_argument('description', type=str)
parser.add_argument('units', type=str)
parser.add_argument('farm_stage', type=str)
parser.add_argument('duration', type=str)
parser.add_argument('start_date', type=str)
parser.add_argument('price', type=str) # price per unit
parser.add_argument('margin', type=str) # profit margin in percentage

class FarmAPI(Resource):
    @jwt_required    
    def post(self):
        args = parser.parse_args()
        name = args['name']
        description = args['description']
        location = args['location']
        units = args['units']
        start_date = args["start_date"]
        margin = args['margin']
        price = args['price']
        duration = args['duration']


        # Validate input data
        if not valid_farm_name(name):
            return raise_error(400, "'name' field missing or invalid")
        if not valid_farm_name(duration):
            return raise_error(400, "'duration' field missing or invalid")
        if not valid_description(description):
            return raise_error(400, "'description' field missing or invalid")
        if not valid_location(location):
            return raise_error(400, "'location' field missing or invalid")
        if not valid_units(units):
            return raise_error(400, "'units' field missing or invalid")
        #
        if not valid_margin(margin):
            return raise_error(400, "'margin' field missing or invalid")
        if not valid_price(price):
            return raise_error(400, "'price' field missing or invalid")
        if not valid_date(start_date):
            return raise_error(400, "'start_date' field missing or invalid")

        farm = Farm(
            name=name, 
            description=description,
            location=location,
            units=units,
            start_date=start_date,
            duration=duration,
            margin=margin,
            price=price,
            user_id=current_user.id
        )
        db.session.add(farm)
        db.session.commit()
        uri = url_for('one-acre.farm', id=farm.id, _external=True)

        output = {}
        output['status'] = 201
        output['message'] = 'Created a new farm'
        data = farm.serialize
        data['uri'] = uri
        output['data'] = [data]

        return output, 201, {'Location': uri}

    @jwt_required    
    def get(self, id=None):
        # Return farm data
        if id is None:
            # Return a collection of all farms
            # all_farms = Farm.query.filter_by(active=True)
            all_farms = Farm.query.all()
            output = {}
            output['status'] = 200
            data = all_farms
            if all_farms:
                data = [farm.serialize for farm in all_farms]
            output['data'] = data

            return output

        if not id.isnumeric():
            return raise_error(400, "Farm ID should be an integer")
        farm_id = int(id)
        farm = Farm.query.filter_by(id=farm_id, active=True)
        if not farm:
            return raise_error(404, "Requested farm does not exist")

        output = {}
        output['status'] = 200
        output['data'] = [farm.serialize]

        return output

    @jwt_required    
    def patch(self, id, field):

        if not id.isnumeric():
            return raise_error(400, "Farm ID should be an integer")
        farm_id = int(id)
        farm = Farm.query.get(farm_id)
        if not farm:
            return raise_error(404, "Farm does not exist")

        if current_user.id != farm.user_id:
            return raise_error(403, 'Request forbidden - you are not allowed'
                               'to access this resource')

        # update farm with given ID
        if not id.isnumeric():
            return raise_error(400, "Farm ID should be an integer")
        if field not in ('name', 'start_date', 'description', 'location',
                         'stage', 'units', 'margin', 'active', 'price'):
            return raise_error(400, "Invalid field name")

        parser = reqparse.RequestParser()
        parser.add_argument(field, type=str, required=True)

        try:
            args = parser.parse_args(strict=True)
        except:
            error_msg = "Please provide the {} field only".format(field)
            return raise_error(400, error_msg)

        new_field_value = args.get(field)
        if field == 'name':
            new_field_value = valid_farm_name(new_field_value)
        elif field == 'units':
            new_field_value = valid_units(new_field_value)
        elif field == 'description':
            new_field_value = valid_description(new_field_value)
        elif field == 'start_date':
            new_field_value = valid_date(new_field_value)
        elif field == 'margin':
            new_field_value = valid_margin(new_field_value)
        elif field == 'stage':
            new_field_value = valid_farm_stage(new_field_value)
        elif field == 'location':
            new_field_value = valid_location(new_field_value)
        elif field == 'active':
            new_field_value = valid_active_status(new_field_value)
        elif field == 'price':
            new_field_value = valid_price(new_field_value)

        if not new_field_value:
            return raise_error(400, "Invalid data in {} field".format(field))


        if not farm:
            return raise_error(404, "Farm does not exist")
        if field == 'name':
            farm.name = new_field_value
        if field == 'description':
            farm.description = new_field_value
        if field == 'start_date':
            farm.start_date = new_field_value
        if field == 'margin':
            farm.margin = new_field_value
        if field == 'stage':
            farm.stage = new_field_value
        if field == 'location':
            farm.location = new_field_value
        if field == 'units':
            farm.units = new_field_value
        if field == 'price':
            farm.price = new_field_value
        if field == 'active':
            farm.active = (False if new_field_value == 'inactive' else
            new_field_value)


        db.session.commit()

        output = {}
        data = farm.serialize
        output['status'] = 200
        data['message'] = 'successfully updated farm {} field'.format(field)
        output['data'] = [data]

        return output

    @admin_required
    @jwt_required
    def delete(self, id):
        # Delete farm with given ID
        if not id.isnumeric():
            return raise_error(400, "Farm ID should be an integer")
        farm_id = int(id)
        farm = Farm.query.get(farm_id)
        if not farm:
            return raise_error(404, "Farm does not exist")
        farm = Farm.query.get(farm_id)

        if current_user.id != farm.user_id:
            return raise_error(403, 'Request forbidden - you are not allowed'
                               'to access this resource')
        db.session.delete(farm)
        db.session.commit()

        output = {}
        message = 'Farm has been deleted'
        output['status'] = 200
        output['data'] = [{'id': farm_id, 'message': message}]
        return output
