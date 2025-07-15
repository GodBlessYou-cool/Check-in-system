# Check-in-system
check-in system used for a unmanned store
# Customer Data Retriever with Purchase Records 🛒🔍

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![API](https://img.shields.io/badge/API-Stickie%20Link-orange)

A Python script that retrieves customer membership data and purchase records through the Stickie Link API. Simply provide a customer's bio link to get detailed member information and aggregated purchase history.

## ✨ Features

- **Member Information Retrieval**: Get name, email, phone number, membership tier, and status
- **Purchase Record Analysis**: Aggregate purchase history by product with quantity totals
- **Bio Link Parsing**: Automatically extracts member identifiers from various URL formats
- **API Authentication**: Handles JWT token authentication and renewal
- **Error Handling**: Comprehensive exception handling with user-friendly error messages

## ⚡ Quick Start

### Prerequisites

- Python 3.8+
- Requests library

### Installation

```bash
pip install requests
```bash

python QR-code.py

Enter a bio link (or 'quit' to exit):
https://stickie.link/bio-link/john-doe

Authenticating...
Authentication successful

=== MEMBER INFORMATION ===
name: John Doe
email: john.doe@example.com
phone: +1 234-567-8901
member_id: MEM12345
tier: Premium
status: Active
join_date: 2023-01-15T08:30:00.000000Z

Retrieving purchase records for John Doe...

=== PURCHASE RECORDS ===
Premium Coffee Beans: 5, last shopping date: 2024-02-15
Stainless Steel Mug: 2, last shopping date: 2024-01-20
Organic Tea Sampler: 3, last shopping date: 2023-12-10

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
