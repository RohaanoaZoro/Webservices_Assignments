
import hmac
import base64
import json
import time
import hashlib

# encoded = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRpZCI6IjNmMzk3OTc5LTE5YjMtNDk3Zi04YTNjLWM0Y2E2ZWUzNzk2MSIsInNlZXNpb25pZCI6ImZkNTRhOWZhLTVhNDktNDkxYi05NDY5LThkMmEwMmYwMjljYiIsImV4cCI6MTY4MzY2NzcwMiwiaWF0IjoxNjgzNjY2ODAyfQ.1j8Y4euwBgoPmKIfS29mPFnm-2OPZjy-Mr4tF4FGGrM"
# public_key = "16ad099a-852e-4967-a5a6-9c1afd3ea89f"

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

# print(verify_jwt(encoded, public_key))
