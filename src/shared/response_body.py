import json

def res_boiler(status_code: int, body: dict[str,str]):
    return {
        'statusCode': status_code,
        'header': {
            'content-type': 'application/json'
        },
        'body': json.dumps(body)
    }

def res_msg(status_code: int, message:str):
    is_error = True if status_code > 299 else False
    if is_error:
        msg = {'error': message}
    else:
        msg = {'message': message}

    return res_boiler(status_code, msg)

def retrieved_item_res(content:dict[str, str]):
    return res_boiler(200, content)

def invalid_request_error_res(msg:str=None):
    return res_msg(400, msg or 'Invalid request body.')

def server_error_res(error: str):
    print(f"FATAL LAMBDA EXECUTION ERROR: {error}")
    return res_msg(500, 'Something went wrong, try again.')

def created_successfully_res(msg:str=None):
    return res_msg(201, msg or 'Item added successfully.')

def request_success_res(msg:str=None):
    return res_msg(200, msg or 'Request completed successfully.')

def not_found_res(msg:str=None):
    return res_msg(404, msg or 'No such item exists.')