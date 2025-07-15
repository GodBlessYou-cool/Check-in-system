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

