'''
API Resource for hello
'''
from flask_restful import Resource


class HelloWorld(Resource):
    '''
    A simple class for a RESTful API endpoint that returns a greeting message.

    Attributes:
    - Resource (class): A base class for RESTful API endpoints.
    '''
    def get(self):
        '''
        Returns a JSON response with a greeting message.

        Returns:
        - dict: A dictionary containing the message as a key-value pair.
        '''
        return {'message': 'Hello, World! v1'}
