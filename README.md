<div align="center">
<h1> Ultimate Point of Sale (POS)</h1>
</div>

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

A modern POS/ERP/CRM system for businesses of the AI era. Powered by [Django.](https://djangoproject.com)

<p align="center">
  <img src="https://github.com/KagemaNjoroge/ultimate_pos/blob/main/django_pos/static/img/logos/UltimatePOS%20Logo(2).svg">
</p>

## Demo

You can access the demo [here](https://pos.tomorrow.co.ke/).
The credentials are:

- `username: demo`
- `password: 12345678`

## Features

- Dashboard Page with statistics and graphs
- DataTables with print, copy, to CSV, and to PDF buttons
- Categories and Products Management
- Clients Management
- Sales Management
- eTIMS(electronic Tax Invoice Management System)

## Proposed Features

- [x] Business Level Inventory Management
- [ ] Lipa-na-MPESA Gateway integration
- [ ] KRA Tax Returns Auto-filing
- [ ] Plugin system
- [x] AI Assistant
- [x] Suppliers Management
- [x] Purchase Management
- [x] CRM (Customer Relationship Management)

## TODOS

- [ ] Add feature to renew subscription
- [ ] Add Lipa na Mpesa Support
- [ ] Update the documentation to document management commands

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

5. Install GTK to create the PDF files:  
   [Official documentation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)

6. Windows:  
   After installing GTK, you need to add it to your system's Path environment variable. Follow these steps:

   - Assuming you installed GTK at:
     `C:\Program Files\GTK3-Runtime Win64\bin`  
     This will be your new variable that you need to add to Path
   - Refer to this tutorial for detailed instructions on adding to the Path environment variable:
     [Adding variable to path](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/)

   - If you encounter an error such as "cannot load library," refer to this documentation for troubleshooting:
     [Missing Library Error](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#missing-library)

7. Restart your computer: After completing the steps above, it is essential to restart your computer for the changes to take effect properly.

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

4.  Make database migrations:

```bash
 python manage.py makemigrations && python manage.py migrate
```

5.  Create superuser to access the admin panel:

> [!IMPORTANT]
> You will need a super user account in order to access the admin page. You can create one by running the following command:

```bash
python manage.py createsuperuser
```

with the following data, or with the data you prefer:

- `username: YOUR_PREFERRED_USERNAME`
- `password: YOUR_PASSWORD`
- `email: YOUR_EMAIL@EMAIL.COM`

6. Run the server:

   ```bash
   python manage.py runserver
   ```

7. Open a browser and navigate : `http://127.0.0.1:8000/`

8. Log In with your superuser credentials.

## Contributing

Contributions are always welcome!

- Fork this repository;

- Create a branch with your feature: `git checkout -b my-feature`;

- Commit your changes: `git commit -m "feat: my new feature"`;

- Push to your branch: `git push origin my-feature`.

  ## License

This project is under [MIT License.](https://choosealicense.com/licenses/mit/)

<div align="center">
Brought to you by the good folks at 
<a href="https://tomorrow.co.ke">TomorrowAI</a>
</div>
