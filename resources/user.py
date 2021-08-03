from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    """
    Register users via POST request
    with login and password
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username is required")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password is required")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "Error: Already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'Success: User created successfully'}, 201
