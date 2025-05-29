import json


def invalid_request_error_res(msg:str=None):
    return {
        'statusCode': 400,
        'body': json.dumps({
            'error': msg or 'Invalid request body.'
        })
    }

def server_error_res(error: str):
    print(f"FATAL LAMBDA EXECUTION ERROR: {error}")
    return {
        'statusCode': 500,
        'body': json.dumps({
            'error': 'Something went wrong, try again.'
        })
    }

def created_successfully_res(msg:str=None):
    return {
        'statusCode': 201,
        'body': json.dumps({
            'message': msg or 'Item added successfully.'
        })
    }

def request_success_res(msg:str=None):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': msg or 'Request completed successfully.'
        })
    }