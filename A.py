import requests
from urllib.parse import urlparse, quote
import json

class CustomerDataRetriever:
    def __init__(self):
        self.API_CONFIG = {
            'login_url': 'https://staging.stickie.link/api/v1/login',
            'member_data_url': 'https://staging.stickie.link/api/v1/membership/member_data',
            'membership_url': 'https://staging.stickie.link/api/v1/membership/data',
            'credentials': {
                'email': 'kishore@stickies.tech',
                'password': 'Abc123'
            },
            'token': None
        }
        self.session = requests.Session()

    def authenticate(self):
        """Authenticate with the API"""
        try:
            response = self.session.post(
                self.API_CONFIG['login_url'],
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                json=self.API_CONFIG['credentials']
            )

            if not response.ok:
                error_data = response.json() if response.text else {}
                raise Exception(error_data.get('message', f'Authentication failed ({response.status_code})'))

            data = response.json()
            if not data.get('token'):
                raise Exception('No authentication token received')

            self.API_CONFIG['token'] = data['token']
            return True

        except Exception as e:
            raise Exception(f'Authentication error: {str(e)}')

    def extract_member_identifier(self, input_data):
        """Extract member identifier from bio link"""
        try:
            url = urlparse(input_data)
            path_segments = [seg for seg in url.path.split('/') if seg.strip()]
            
            for i, segment in enumerate(path_segments):
                if segment.lower() in ['bio-link', 'member'] and i + 1 < len(path_segments):
                    return path_segments[i + 1].split('?')[0]
                
            if path_segments:
                return path_segments[-1].split('?')[0]
            
            return None

        except:
            return None

    def get_member_data(self, identifier):
        """Get basic member information"""
        try:
            if not self.API_CONFIG['token']:
                self.authenticate()

            query_params = [
                f'link={quote(identifier)}',
                f'username={quote(identifier)}',
                f'id={quote(identifier)}',
                f'member_id={quote(identifier)}'
            ]
            
            for param in query_params:
                url = f"{self.API_CONFIG['membership_url']}?{param}"
                
                response = self.session.get(
                    url,
                    headers={
                        'Authorization': f"Bearer {self.API_CONFIG['token']}",
                        'Accept': 'application/json'
                    }
                )
                
                if response.ok:
                    data = response.json()
                    member = self.find_member_in_response(data, identifier)
                    if member:
                        return self.format_member_data(member)
            
            raise Exception('Member not found')

        except Exception as e:
            return {
                'error': True,
                'message': str(e)
            }

    def get_purchase_records(self, member_identifier):
        """Get purchase records for a member using GET request"""
        try:
            if not self.API_CONFIG['token']:
                self.authenticate()

            url = f"{self.API_CONFIG['member_data_url']}?link={quote(member_identifier)}"
            
            response = self.session.get(
                url,
                headers={
                    'Authorization': f"Bearer {self.API_CONFIG['token']}",
                    'Accept': 'application/json'
                }
            )

            if not response.ok:
                error_data = response.json() if response.text else {}
                raise Exception(error_data.get('message', f'API request failed ({response.status_code})'))

            data = response.json()
            return self.filter_purchase_data(data)

        except Exception as e:
            return {
                'error': True,
                'message': str(e)
            }

    def filter_purchase_data(self, data):
        """Extract relevant product information from purchase records and aggregate quantities"""
        if not data.get('data') or not data['data'].get('user'):
            return []

        orders = data['data']['user'].get('orders', [])
        product_totals = {}

        for order in orders:
            for product in order.get('order_products', []):
                product_info = product['product']
                product_name = product_info.get('name')
                quantity = product['product_quantity']
                last_shopping_date = order.get('paid_date')[:10]  # Format date to YYYY-MM-DD

                if product_name in product_totals:
                    product_totals[product_name]['quantity'] += quantity
                else:
                    product_totals[product_name] = {
                        'quantity': quantity,
                        'last_shopping_date': last_shopping_date
                    }

        # Convert the dictionary to a list of records for easier processing
        return [
            {'product_name': name, 'quantity': details['quantity'], 'last_shopping_date': details['last_shopping_date']}
            for name, details in product_totals.items()
        ]

    def find_member_in_response(self, data, identifier):
        """Find member in API response"""
        search_id = identifier.lower()
        candidates = []

        if data.get('data', {}).get('data'):
            candidates.extend(data['data']['data'])
        if isinstance(data.get('data'), list):
            candidates.extend(data['data'])
        if data.get('user_data'):
            candidates.append(data['user_data'])
        if data.get('data'):
            candidates.append(data['data'])
        
        for member in candidates:
            member_id = str(member.get('link') or member.get('username') or 
                             member.get('id') or member.get('member_id') or '').lower()
            if search_id == member_id:
                return member
        
        return None

    def format_member_data(self, member):
        """Format member data for display"""
        user = member.get('user', {})
        return {
            'name': user.get('name') or member.get('name') or 'Not available',
            'email': user.get('email') or member.get('email') or 'Not provided',
            'phone': user.get('phone') or member.get('phone') or 'Not provided',
            'member_id': member.get('member_id') or member.get('id') or 'N/A',
            'tier': member.get('tier', {}).get('name') or 'Standard',
            'status': 'Active' if member.get('status') == 1 else 'Inactive',
            'join_date': member.get('created_at', 'Unknown')
        }

    def process_bio_link(self, bio_link):
        """Process a bio link and return complete member data"""
        try:
            identifier = self.extract_member_identifier(bio_link)
            if not identifier:
                return {'error': 'Invalid bio link format'}
            
            member_data = self.get_member_data(identifier)
            if isinstance(member_data, dict) and member_data.get('error'):
                return {'error': member_data['message']}
            
            return {
                'status': 'success',
                'member_data': member_data
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

def display_results(result):
    """Display the results in a readable format"""
    if result.get('status') == 'success':
        print("\n=== MEMBER INFORMATION ===")
        for key, value in result['member_data'].items():
            print(f"{key}: {value}")
        
    else:
        print(f"\nError: {result.get('message')}")

def main():
    retriever = CustomerDataRetriever()
    
    while True:
        print("\nEnter a bio link (or 'quit' to exit):")
        bio_link = input().strip()
        
        if bio_link.lower() == 'quit':
            break
            
        try:
            print("Authenticating...")
            retriever.authenticate()
            print("Authentication successful")
        except Exception as e:
            print(f"Authentication failed: {e}")
            continue
            
        result = retriever.process_bio_link(bio_link)
        display_results(result)

        if result.get('status') == 'success':
            member_name = result['member_data']['name']
            print(f"\nRetrieving purchase records for {member_name}...")
            purchase_records = retriever.get_purchase_records(member_name)
            
            if isinstance(purchase_records, dict) and purchase_records.get('error'):
                print(f"Error retrieving purchase records: {purchase_records['message']}")
            else:
                print("\n=== PURCHASE RECORDS ===")
                for record in purchase_records:
                    product_name = record['product_name']
                    quantity = record['quantity']
                    last_shopping_date = record['last_shopping_date']
                    print(f"{product_name}: {quantity}, last shopping date: {last_shopping_date}")

if __name__ == "__main__":
    print("Customer Data Retriever with Purchase Records")
    print("-------------------------------------------")
    main()