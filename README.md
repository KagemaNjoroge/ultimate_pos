## Ultimate Point of Sale (POS)

A minimalistic Point of Sale (POS) system for small businesses. It is a web-based application that allows you to manage your sales and inventory on the go. It is built with Django and Python.

<div style="text-align: center"><a><img src="screenshots\dashboard.png" width="70%" alt="Ultimate POS Dashboard"/></a></div>
<br></br>
<div style="text-align: center"><a><img src="screenshots\sales.png" width="70%" alt="Ultimate POS Sales Page"/></a></div>

## Table of Contents:

- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Run it locally](#run-it-locally)
- [Contributing](#contributing)
- [License](#license)

## Features

- Login Page with User authentication
- Dashboard Page with statistics and graphs
- DataTables with print, copy, to CSV, and to PDF buttons
- Categories and Products Management
- Clients Management
- Sales Management
- eTIMS(electronic Tax Invoice Management System)

## Proposed Features

- BUsiness Level Inventory Management
- Suppliers Management
- Purchase Management
- CRM (Customer Relationship Management)

## Tech Stack

- Frontend:
  - HTML
  - CSS
  - JavaScript
  - Boostrap
  - SweetAlert
  - DataTables
- Backend:
  - Django
  - Python
  - Ajax
  - SQLite

## Installation

#### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [pip package manager](https://pip.pypa.io/en/stable/installation/)
- [git](https://git-scm.com/downloads)

<br>

1. Clone or download the repository:

```bash
git clone https://github.com/kagemanjoroge/ultimate_pos.git
```

2. Go to the project directory

```bash
cd ultimate_pos
```

3. Create a virtual environment :

```bash
python3 -m venv venv
source venv/bin/activate
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
     [Adding varible to path](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/)

   - If you encounter an error such as "cannot load library," refer to this documentation for troubleshooting:
     [Missing Library Error](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#missing-library)

7. Restart your computer: After completing the steps above, it is essential to restart your computer for the changes to take effect properly.

## Run it locally

After restarting your computer

1. Go to the project directory: `cd ultimate_pos`

2. Activate the virtual enviroment

   ```bash
   source venv/bin/activate
   ```

3. Go to the django_pos folder:

   ```bash
   cd ultimate_pos/django_pos
   ```

4. Make database migrations:

```bash
python manage.py makemigrations && python manage.py migrate
```

5. Create superuser to access the admin panel:

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

## Authors

- [@kagemanjoroge](https://github.com/kagemanjoroge)
