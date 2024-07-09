import hashlib
import hmac
import json
from urllib.parse import parse_qs

def verify_webapp_data(init_data, bot_token):
    try:
        parsed_data = parse_qs(init_data)
        received_hash = parsed_data.get('hash', [''])[0]
        data_check_string = '\n'.join([f"{k}={v[0]}" for k, v in parsed_data.items() if k != 'hash'])
        secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        return calculated_hash == received_hash
    except Exception as e:
        print(f"Error verifying WebApp data: {e}")
        return False

def get_user_info(init_data):
    try:
        parsed_data = parse_qs(init_data)
        user_json = parsed_data.get('user', ['{}'])[0]
        return json.loads(user_json)
    except Exception as e:
        print(f"Error parsing user info: {e}")
        return None
