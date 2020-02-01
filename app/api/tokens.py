from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse, request
from app.exceptions import TokenNotFound
from app.helpers import get_user_tokens, revoke_token, unrevoke_token, prune_database
from app.decorators import admin_required
from .common.utils import valid_email, valid_password
from .common.errors import raise_error

class Tokens(Resource):
    # Provide a way for a user to look at their tokens
    @jwt_required
    def get(self):
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)
        data = [token.serialize for token in all_tokens]

        response = {}
        response['status'] = 201
        response['data'] = data

        return response

    @jwt_required
    def put(self, token_id):
        parser = reqparse.RequestParser()
        parser.add_argument('revoke', type=bool)
        # Get and verify the desired revoked status from the body
        args = parser.parse_args()
        if not args:
            return raise_error(400, "Missing 'revoke' in body")
        revoke = args.get('revoke', None)
        if revoke is None:
            return raise_error(400, "Missing 'revoke' in body")
        if not isinstance(revoke, bool):
            return raise_error(400, "'revoke' must be a boolean")

        # Revoke or unrevoke the token based on what was passed to this function
        user_identity = get_jwt_identity()
        try:
            if revoke:
                revoke_token(token_id, user_identity)
                return  {'status': 200, 'message': "Token successfully revoked"}
            unrevoke_token(token_id, user_identity)
            return  {'status': 200, 'message': "Token successfully revoked"}
        except TokenNotFound:
            return raise_error(404, 'The specified token was not found')
    
    @jwt_required
    @admin_required
    def delete(self):
        """
        Delete all expired tokens from blacklist database
        """
        prune_database()

        return {
                "status": 200,
                "message": "Blacklist database successfully pruned"
                }

