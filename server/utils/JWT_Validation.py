import jwt
from ..config import key


# Validate the jwt token, check if authorized for the target url
# If authorized, return Authorized msg and the payload.
# Otherwise, return the payload (validation successful) or Fail msg
def jwt_validation(token, taget_url):
    # If token exist, try decode the token
    if token != None:
        try:
            payload = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            pass
        except jwt.DecodeError:
            pass
        # If successfully decoded, check if permission for target url granted
        else:
            # If permission granted, return Authorized and the payload
            if 'index' in taget_url and payload['index_page_authorization']:
                return {'msg': 'Authorized',
                        'data': {'payload': payload}}
            if 'edit' in taget_url and payload['edit_page_authorization']:
                return {'msg': 'Authorized',
                        'data': {'payload': payload}}
            # If permission not granted, return Unauthorized and the payload
            return {'msg': 'Unauthorized',
                    'data': {'payload': payload}}
    # If validation failed, return Validation failed
    return {'msg': 'Validation failed',
            'data': None}
