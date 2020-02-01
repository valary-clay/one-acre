
"""
app.api.funded_funded_farms
~~~~~~~~~~~~~~~~~

"""

from flask_restful import Resource, reqparse, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from sqlalchemy import or_
from app.models import FundedFarm, Farm
from app import db
from .common.errors import raise_error
from .common.utils import (
    valid_farm_name, valid_status, valid_price
)
from app.decorators import admin_required

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('status', type=str)
parser.add_argument('amount', type=str)
parser.add_argument('units', type=str)
parser.add_argument('payout', type=str)
parser.add_argument('id', type=str)

class FundedFarmAPI(Resource):
    @jwt_required    
    def post(self):
        args = parser.parse_args()
        name = args['name']
        status = args['status']
        amount = args['amount']
        units = args['units']
        payout = args['payout']
        id = args.get('id')
        farm_id = int(id)

        name = valid_farm_name(name)
        status = valid_status(status)
        amount = valid_price(amount)
        units = valid_price(units)
        payout = valid_price(payout)

        # Validate input data
        if name is None:
            return raise_error(400, "'name' field missing or invalid")
        if status is None:
            return raise_error(400, "'status' field missing or invalid")
        if amount is None:
            return raise_error(400, "'amount' field missing or invalid")
        if units is None:
            return raise_error(400, "'units' field missing or invalid")
        if payout is None:
            return raise_error(400, "'payout' field missing or invalid")

        funded_farm = FundedFarm(
            name=name, 
            status=status,
            amount=amount,
            units=units,
            payout=payout,
            user_id=current_user.id,
            farm_id=farm_id
        )
        farm_to_update = Farm.query.filter_by(id=farm_id).first()
        if farm_to_update:
            initial_units = int(farm_to_update.units)
            farm_to_update.units = (initial_units - units)
            farm_to_update.status = "pending"
        db.session.add(funded_farm)
        db.session.commit()

        output = {}
        output['status'] = 201
        output['message'] = 'Funded a new farm'
        data = funded_farm.serialize
        output['data'] = [data]

        return output, 201

    @jwt_required    
    def get(self, id=None):
        # Return funded_farm data
        if id is None:
            # Return a collection of all funded_farms
            # that are pending or confirmed
            all_funded_farms = FundedFarm.query.filter(
                FundedFarm.user_id==current_user.id
            ).all()
            output = {}
            output['status'] = 200
            data = all_funded_farms
            if all_funded_farms:
                data = [funded_farm.serialize for funded_farm in all_funded_farms]
            output['data'] = data

            return output

        if not id.isnumeric():
            return raise_error(400, "FundedFarm ID should be an integer")
        funded_farm_id = int(id)
        funded_farm = FundedFarm.query.filter_by(id=funded_farm_id,
                                                 user_id=current_user.id)
        if not funded_farm:
            return raise_error(404, "Requested funded farm does not exist")

        output = {}
        output['status'] = 200
        output['data'] = [funded_farm.serialize]

        return output

    @admin_required
    @jwt_required    
    def patch(self, id, field):

        if not id.isnumeric():
            return raise_error(400, "FundedFarm ID should be an integer")
        funded_farm_id = int(id)
        funded_farm = FundedFarm.query.get(funded_farm_id)
        if not funded_farm:
            return raise_error(404, "FundedFarm does not exist")

        if current_user.id != funded_farm.user_id:
            return raise_error(403, 'Request forbidden - you are not allowed'
                               'to access this resource')

        # update funded_farm with given ID
        if not id.isnumeric():
            return raise_error(400, "FundedFarm ID should be an integer")
        if field not in ('status'): 
            return raise_error(400, "Invalid field name - Please provided a status field")

        parser = reqparse.RequestParser()
        parser.add_argument(field, type=str, required=True)

        try:
            args = parser.parse_args(strict=True)
        except:
            error_msg = "Please provide the {} field only".format(field)
            return raise_error(400, error_msg)

        status = args.get(field)
        status = valid_status(status)

        if status is None:
            return raise_error(400, "Invalid status name - should be one of"
                               "inactive', 'pending', or 'confirmed'")
        funded_farm.status = status

        db.session.commit()

        output = {}
        data = funded_farm.serialize
        output['status'] = 200
        data['message'] = 'successfully updated status field'.format(field)
        output['data'] = [data]

        return output

    @admin_required
    @jwt_required
    def delete(self, id):
        # Delete funded_farm with given ID
        if not id.isnumeric():
            return raise_error(400, "FundedFarm ID should be an integer")
        funded_farm_id = int(id)
        funded_farm = FundedFarm.query.get(funded_farm_id)
        if not funded_farm:
            return raise_error(404, "FundedFarm does not exist")

        if current_user.id != funded_farm.user_id:
            return raise_error(403, 'Request forbidden - you are not allowed'
                               'to access this resource')
        db.session.delete(funded_farm)
        db.session.commit()

        output = {}
        message = 'FundedFarm has been deleted'
        output['status'] = 200
        output['data'] = [{'id': funded_farm_id, 'message': message}]
        return output
