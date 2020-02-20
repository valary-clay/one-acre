"""
app.api.users
~~~~~~~~~~~~~~~~~

"""

from flask_restful import Resource, reqparse, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app.models import User
from app import db
from .common.errors import raise_error
from app.decorators import admin_required

parser = reqparse.RequestParser()
parser.add_argument('email', type=str)
parser.add_argument('bank_name', type=str)
parser.add_argument('bank_account_num', type=str)
parser.add_argument('bank_account_name', type=str)
parser.add_argument('role', type=str)
parser.add_argument('admin', type=bool)
parser.add_argument('first_name', type=str)
parser.add_argument('last_name', type=str)
parser.add_argument('id_num', type=int)

class Users(Resource):
    @jwt_required
    @admin_required
    def post(self):
        args = parser.parse_args()
        email = args['email']
        bank_name = args['bank_name']
        bank_account_num = args['bank_account_num']
        bank_account_name = args['bank_account_name']
        role = args['role']
        admin = args['admin']

        user = User(
            email=email,
            bank_name=bank_name,
            bank_account_num=bank_account_num,
            role=role,
            bank_account_name=bank_account_name,
            admin=admin
        )



        db.session.add(user)
        db.session.commit()
        uri = url_for('one-acre.user', id=user.id, _external=True)

        output = {}
        output['status'] = 201
        output['message'] = 'Created a new user'
        data = user.serialize
        data['uri'] = uri
        output['data'] = [data]

        return output, 201, {'Location': uri}

    @jwt_required
    @admin_required
    def get(self, id=None):
        # Return user data
        if id is None:
            # Return a collection of all users
            all_users = User.query.all()
            output = {}
            output['status'] = 200
            data = all_users
            if all_users:
                data = [user.serialize for user in all_users]
            output['data'] = data

            return output

        if not id.isnumeric():
            return raise_error(400, "User ID should be an integer")
        user_id = int(id)
        user = User.query.get(user_id)
        if not user:
            return raise_error(404, "Requested user does not exist")

        output = {}
        output['status'] = 200
        output['data'] = [user.serialize]

        return output

    @jwt_required
    def patch(self, id, field):

        if not id.isnumeric():
            return raise_error(400, "User ID should be an integer")
        user_id = int(id)
        user = User.query.get(user_id)
        if not user:
            return raise_error(404, "User does not exist")

        if current_user.id != user.id:
            return raise_error(403, 'Request forbidden - you are not allowed'
                               'to access this resource')

        # update user with given ID
        if not id.isnumeric():
            return raise_error(400, "User ID should be an integer")
        if field not in ('bank_name', 'bank_account_num', 'bank_account_name',
                         'role','admin', 'email', 'first_name', 'last_name', 'id_num'):
            return raise_error(400, "Invalid field name")

        parser = reqparse.RequestParser()
        parser.add_argument(field, type=str, required=True)

        try:
            args = parser.parse_args(strict=True)
        except:
            error_msg = "Please provide the {} field only".format(field)
            return raise_error(400, error_msg)

        new_field_value = args.get(field)
        if not new_field_value:
            return raise_error(400, "Invalid data in {} field".format(field))


        if not user:
            return raise_error(404, "User does not exist")
        if field == 'first_name':
            user.first_name = new_field_value
        if field == 'last_name':
            user.last_name = new_field_value
        if field == 'id_num':
            new_field_value = int(new_field_value)
            user.id_num = new_field_value
        if field == 'bank_name':
            user.bank_name = new_field_value
        if field == 'bank_account_num':
            user.bank_account_num = new_field_value
        if field == "bank_account_name":
            user.bank_account_name = new_field_value
        if field == 'role':
            user.role = new_field_value
        if field == 'email':
            user.email = new_field_value
        if field == 'admin':
            user.admin = bool(new_field_value)

        db.session.commit()

        output = {}
        data = user.serialize
        output['status'] = 200
        data['message'] = 'successfully updated user {} field'.format(field)
        output['data'] = [data]

        return output

    @jwt_required
    @admin_required
    def delete(self, id):
        # Delete user with given ID
        if not id.isnumeric():
            return raise_error(400, "User ID should be an integer")
        user_id = int(id)
        user = User.query.get(user_id)
        if not user:
            return raise_error(404, "User does not exist")
        user = User.query.get(user_id)

        if current_user.id != user.user_id:
            return raise_error(403, 'Request forbidden - you are not allowed'
                               'to access this resource')
        db.session.delete(user)
        db.session.commit()

        output = {}
        message = 'User has been deleted'
        output['status'] = 200
        output['data'] = [{'id': user_id, 'message': message}]
        return output
