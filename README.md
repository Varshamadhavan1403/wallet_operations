# Wallet Transaction System

This is a Django REST Framework-based financial application that supports wallet transactions. The system ensures atomic transactions and includes user validation during user creation. The application also supports JWT authentication.

## Features

- User registration with wallet creation
- Wallet balance retrieval
- Wallet deposit and withdrawal
- Transaction history retrieval
- JWT-based authentication
- Atomic transactions to ensure data integrity

## Requirements

- Python 3.x
- Django 3.x or 4.x
- Django REST Framework
- Django REST Framework Simple JWT

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/wallet-transaction-system.git
   cd wallet-transaction-system
2. **Create and activate venv**
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. **Install the dependencies**
    pip install -r requirements.txt
4. **Run migrations**
    python manage.py migrate
5. **Create superuser**
    python manage.py createsuperuser
6. **Start development server**
    python manage.py runserver
7. **Configuration JWT Settings**
    **Configure JWT settings in your settings.py**

    from datetime import timedelta

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
        'ROTATE_REFRESH_TOKENS': False,
        'BLACKLIST_AFTER_ROTATION': True,
        'ALGORITHM': 'HS256',
        'SIGNING_KEY': SECRET_KEY,
        'AUTH_HEADER_TYPES': ('Bearer',),
    }
8. **Usage**
    **Register a new user**
        POST /api/register/
    {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
9. **Obtain jwt token**

    POST /api/token/
    {
        "username": "testuser",
        "password": "testpassword"
    }
10. **Refresh jwt token**
    POST /api/token/refresh/
    {
        "refresh": "your_refresh_token"
    }
11. **Deposit to wallet**

    POST /api/wallet/deposit/
    Authorization: Bearer your_access_token
    {
        "amount": 100.00
    }
12. **Withdraw from wallet**
    POST /api/wallet/withdraw/
    Authorization: Bearer your_access_token
    {
        "amount": 50.00
    }
13. **Retreive wallet balance**
    GET /api/wallet/balance/
    Authorization: Bearer your_access_token
14. **Retrieve Transaction History**
    GET /api/wallet/transactions/
    Authorization: Bearer your_access_token
15. **Testing**
    **Run the tests using the following command**
    python manage.py test
15. **Contributing**
    Fork the repository
    Create a new branch (git checkout -b feature/your-feature)
    Commit your changes (git commit -am 'Add some feature')
    Push to the branch (git push origin feature/your-feature)
    Create a new Pull Request
## Contributors

- [VARSHA MADHAVAN](https://github.com/Varshamadhavan1403)



