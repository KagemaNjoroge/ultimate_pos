<p align="center">
  <img src="./django_pos//static/img/icons/icon512.png" alt="Ultimate POS Logo" >
</p>

A simple, powerful and easy to use Point of Sale (POS) system.

## Features

- Dashboard Page with statistics and graphs
- Products, Product categories Management
- Customers Management
- Suppliers Management
- Sales Management
- Stripe, PayPal, Cash and M-Pesa payment methods
- Support for multiple branches
- Role Based Access Control (RBAC)

## Installation

The Ultimate POS application can be installed using Docker or manually.

### Docker Installation

For Docker installation, follow the [Docker Setup Guide](./DOCKER_SETUP.md).

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kagemanjoroge/ultimate_pos.git && cd ultimate_pos/django_pos
   ```
2. Create a virtual environment, activate it, and install the requirements:
   ```bash
   python3 -m venv venv; source venv/bin/activate; pip install -r requirements.txt
   ```
3. Create a `.env` file based on the `.example.env` template:
   ```bash
   cp .example.env .env
   ```
4. Update the `.env` file with your database credentials and other settings.
5. Run the migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser account:
   ```bash
   python manage.py createsuperuser
   ```
7. Collect static files:
   ```bash
   python manage.py collectstatic --no-input
   ```
8. Start the development server:
   ```bash
   python manage.py runserver
   ```
9. Access the application at http://localhost:8000
10. Rock and roll!
