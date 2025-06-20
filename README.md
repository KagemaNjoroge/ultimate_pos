<p align="center">
  <img src="./django_pos//static/img/icons/icon512.png" alt="Ultimate POS Logo" >
</p>

<div>
   <a href="#features">Features</a>
   <span> | </span>
   <a href="#proposed-features">Proposed Features</a>
   <span> | </span>
   <a href="#installation">Installation</a>
   <span> | </span>
   <a href="#run-it-locally">Run it locally</a>
   <span> | </span>
   <a href="#contributing">Contributing</a>
   <span> | </span>
   <a href="#license">License</a>

</div>
A simple, powerful and easy to use Point of Sale (POS) system.

## Features

- Dashboard Page with statistics and graphs
- DataTables with print, copy, to CSV, and to PDF buttons
- Categories and Products Management
- Clients Management
- Sales Management
- Stripe, PayPal, Cash and M-Pesa payment methods

## Installation

1. Clone or download the repository:

```bash
git clone https://github.com/kagemanjoroge/ultimate_pos.git
```

2. Go to the project directory

```bash
cd ultimate_pos/django_pos
```

3. Create a virtual environment :

```bash
python3 -m venv venv && source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run it locally

After restarting your computer

1.  Go to the project directory: `cd ultimate_pos`

2.  Activate the virtual enviroment

    ```bash
    source venv/bin/activate
    ```

3.  Go to the django_pos folder:

    ```bash
    cd ultimate_pos/django_pos
    ```

4.  Copy the .env.example file to .env:
    Replace the values with your own values

    ```bash
    cp .env.example .env
    ```

5.  Make database migrations:

    ```bash
    python manage.py makemigrations && python manage.py migrate
    ```

6.  Create superuser to access the admin panel:

> [!IMPORTANT]
> You will need a super user account in order to access the admin page. You can create one by running the following command:

    ```bash
    python manage.py createsuperuser
    ```

with the following data, or with the data you prefer:

- `username: YOUR_PREFERRED_USERNAME`
- `password: YOUR_PASSWORD`
- `email: YOUR_EMAIL@EMAIL.COM`

8. Run the server:

   ```bash
   python manage.py runserver
   ```

9. Open a browser and navigate : `http://127.0.0.1:8000/`

10. Log In with your superuser credentials.

## Contributing

Contributions are always welcome!

- Fork this repository;

- Create a branch with your feature: `git checkout -b my-feature`;

- Commit your changes: `git commit -m "feat: my new feature"`;

- Push to your branch: `git push origin my-feature`.

## License

This project is under [MIT License.](https://choosealicense.com/licenses/mit/)
