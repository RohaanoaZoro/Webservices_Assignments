
import hmac
import base64
import json
import time
import hashlib

encoded = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRpZCI6IjEwMDAyIiwic2Vlc2lvbmlkIjoiODYxNjQ1YjItZTg4Mi00NTNkLTk0Y2UtN2MwYTI2ZGJkNzRmIiwiZXhwIjoxNjgyMDEzNzE2fQ.D_asM7zgykqK4aqpM6GpiD3BQtAy4vH8fqp0jQQPzaI"
public_key = "869dd801-5ee1-40ed-b9f3-cb173c404ed3"

def verify_jwt(token, secret_key):

    try:
        # Split the token into its parts
        header_b64, claims_b64, signature_b64 = token.split('.')
    except:
        return {"error_msg":"Error in parsing token"}, True
    
    # Decode the header and claims from base64
    header = json.loads(base64.urlsafe_b64decode(header_b64 + '==').decode())
    claims = json.loads(base64.urlsafe_b64decode(claims_b64 + '==').decode())
    
    # Verify the signature using HMAC-SHA256
    message = f"{header_b64}.{claims_b64}"
    expected_signature = hmac_sha256(message, secret_key.encode())
    if signature_b64 != expected_signature:
        return {"error_msg":"Invalid signature"}, True
    
    # Verify the expiration time
    now = time.time()
    if 'exp' in claims and claims['exp'] < now:
        return {"error_msg":"Token expired"}, True
    
    # Verify the issuer
    if 'iss' in claims and claims['iss'] != "myapp":
        return {"error_msg":"Invalid issuer"}, True
    
    return claims, False
    
def hmac_sha256(data, key):
    return base64.urlsafe_b64encode(hmac.new(key, data.encode(), hashlib.sha256).digest()).decode().rstrip("=")

print(verify_jwt(encoded, public_key))
