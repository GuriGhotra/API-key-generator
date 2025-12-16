from flask import Blueprint, request, jsonify
import requests
from Database.database import get_db_conn

# creating blueprint for the app
countries_api = Blueprint('countries_api', __name__)


# Rest Countries URL
BASE_URL = " https://restcountries.com/v3.1"


# validating api key
def key_validation(api_key):

    # checking db for key
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
        " SELECT user_id, is_active FROM api_keys WHERE api_key = ? ",
        (api_key,))

        key_data = cursor.fetchone()

        # If key doesn't exist or not active
        if not key_data or not key_data['is_active']:
            return False
        
        # Updating the keys usage time
        cursor.execute(
            "UPDATE api_keys SET last_used = datetime('now', 'localtime') WHERE api_key = ?",
            (api_key,)
        )
        conn.commit()

        return True
    except Exception as e:
        print(f'Error validating key: {e}')
        return False
    finally:
        conn.close()

    

@countries_api.route('/country/<country_name>', methods = ['GET'])
def get_countries_info(country_name):

    # checking key is avaialble in headers
    api_key = request.headers.get('X-API-KEY')

    if not api_key:
        return jsonify({'error': 'Missing API key'}), 401
    
    # key validation
    if not key_validation(api_key):
        return jsonify({'error': 'Key is not active or invalid'}), 403
    
    # error handling
    try:
        # Fecthing info frorm rest countries logic
        response = requests.get(f"{BASE_URL}/name/{country_name}")
        if response.status_code != 200:
            return jsonify({'error': 'Country not found'}), 404
        
        country_info = response.json()[0] # First result

        formatted_data = {
            'name': country_info.get('name', {}).get('common','N/A'),
            'official_name': country_info.get('name', {}).get('official','N/A'),
            'capital': country_info.get('capital', ['N/A'])[0] if country_info.get('capital') else 'N/A',
            'currencies': [],
            'languages': [],
            'flag': country_info.get('flags', {}.get('png', 'N/A'))
        }
        

        # Currencies data process
        if 'currencies' in country_info:
            for currency_code, currency_info in country_info['currencies'].items():
                formatted_data['currencies'].append({
                    'code': currency_code,
                    'name': currency_info.get('name', 'N/A'),
                    'symbol': currency_info.get('symbol', 'N/A')
                })
 
        # Languages logic
        if 'languages' in country_info:
            formatted_data['languages'] = list(country_info['languages'].values())


        return jsonify(formatted_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch country data: str{e}'}), 500
    except Exception as e:
        return jsonify({'error': f' Error occured: {str(e)}'}), 500