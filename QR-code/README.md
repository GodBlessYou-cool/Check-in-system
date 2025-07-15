Customer Data Retriever with Purchase Records


Project Overview:

The CustomerDataRetriever is a Python script designed to retrieve customer data and purchase records from a specific API. Users can input a customer's bio link via the command - line. The program will automatically extract the member identifier, fetch the customer's basic information and purchase records, and display the results in a readable format.

Features:

Authentication: Authenticate with the API using the provided email and password to ensure secure data access.
Member Identifier Extraction: Smartly extract the member identifier from the input bio link, supporting various link formats.
Member Information Retrieval: Retrieve the member's basic information, such as name, email, and phone number, based on the extracted member identifier.
Purchase Record Retrieval: Fetch the member's purchase records according to the member identifier, and filter and aggregate the data to show only relevant product information.
Error Handling: Implement comprehensive error handling during authentication, API requests, and data processing, providing detailed error messages.

Installation Dependencies:

This project depends on the requests library. You can install it using the following command:
pip install requests

Code Structure

Main Classes and Functions

CustomerDataRetriever Class:
This class is responsible for interacting with the API and contains the following main methods:

__init__(): Initialize the API configuration and session, setting the login URL, member data URL, membership information URL, and authentication credentials.
authenticate(): Send an authentication request to the API to obtain an authentication token.
extract_member_identifier(input_data): Extract the member identifier from the input bio link.
get_member_data(identifier): Retrieve the member's basic information based on the member identifier.
get_purchase_records(member_identifier): Retrieve the member's purchase records based on the member identifier.
filter_purchase_data(data): Filter and aggregate the purchase record data to extract relevant product information.
find_member_in_response(data, identifier): Find the matching member information in the API response.
format_member_data(member): Format the member information for display.
process_bio_link(bio_link): Process the bio link and return the complete member data.

display_results(result) Function
Display the processed results in a readable format on the console.

main() Function
The entry point of the program, providing a command - line interface that allows users to input bio links and process requests.


Usage

Ensure that you have installed the required dependencies.
Run the script:
python A.py
Follow the prompt to input the customer's bio link, or enter quit to exit the program.
The program will automatically authenticate. If the authentication is successful, it will display the member's basic information.
If the member information is retrieved successfully, the program will attempt to retrieve and display the member's purchase records.

Configuration Instructions

You can modify the following configuration in the __init__ method of the CustomerDataRetriever class:
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

login_url: The login URL of the API.
member_data_url: The URL for retrieving member purchase records.
membership_url: The URL for retrieving member basic information.
credentials: The email and password used for authentication.

Error Handling

If an error occurs during authentication, API requests, or data processing, the program will display the corresponding error message. You can debug and fix the issues based on the error message.
Notes
Make sure that your API configuration information (such as URL, email, and password) is correct.
Since the API may have access restrictions, ensure that your request frequency is within the allowed range.

Contribution

If you find any issues or have improvement suggestions, please feel free to submit issues or pull requests.

License

This project is licensed under the MIT License. Please refer to the LICENSE file for more information.
