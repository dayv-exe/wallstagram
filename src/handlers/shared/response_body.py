import json


def invalid_request_error_res():
    return {
        'statusCode': 400,
        'body': json.dumps({
            'error': 'Invalid request body.'
        })
    }

def server_error_res():
    return {
        'statusCode': 500,
        'body': json.dumps({
            'error': 'Something went wrong, try again.'
        })
    }

def created_successfully_res():
    return {
        'statusCode': 201,
        'body': json.dumps({
            'message': 'Item added successfully.'
        })
    }