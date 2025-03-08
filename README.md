![Django](https://img.shields.io/badge/Django-3.x-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Postgres](https://img.shields.io/badge/Postgres-12.x-blue)
![Django Rest Framework](https://img.shields.io/badge/DRF-3.x-red)

# Companies API in Django and Vue

An API written in Django which would show all company data mostly from India.

## Features

- User authentication and authorization

## Requirements

- Python 3.12
- Django 5.1.4
- Django Rest Framework
- Postgresql
- Node 23.7
- Vue 3.5.13

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/apfirebolt/django_companies.git
    cd django_companies
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Deployment

Install guvicorn server on your server

```
pip install guvicorn
```

```
gunicorn django_companies.wsgi:application 
```

To run the Gunicorn application in the background using `nohup`, use the following command:

Bash 

```
nohup gunicorn django_companies.wsgi:application &
```

Deployment through a service is in progress and would be added in near future. Also working on SSL implementation on the server.

To kill the application running through nohup use grep, search the process ID of the running application and kill it.

```
ps aux | grep "gunicorn django_companies.wsgi:application" | grep -v grep 

kill PID
```

- Access the API at `http://127.0.0.1:8000/api/companies/`
- Use the Django admin interface at `http://127.0.0.1:8000/admin/` to manage companies

## API Endpoints

- `GET /api/companies/` - List all companies

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
