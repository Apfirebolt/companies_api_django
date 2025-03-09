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


## Improvements

Search on name and head_quarters columns

Before Indexing

search on 'reliance' completed in anywhere between 16 to 30 ms without indexing

Generic api calls without search took anywhere between 15 to 25 ms

After indexing no significant improvement was achieved maybe 10%.

After applying Redis cache, it improved the response time from 25ms to 5ms max.

```Python
class ListCompaniesApiView(ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["name", "head_quarters",]
    ordering_fields = ["name", "rating", "company_type", "head_quarters"]
    search_fields = ["name", "head_quarters"]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Company.objects.all()
    
    def get(self, request, *args, **kwargs):

        cache_key = self.generate_cache_key(request)
        cached_data = cache.get(cache_key)

        if cached_data:
            return self.handle_cached_data(cached_data)

        response = super().get(request, *args, **kwargs)

        if response.status_code == 200:
            self.cache_response(cache_key, response.data)

        return response
    
    def generate_cache_key(self, request):
        """Generates a unique cache key based on the request."""
        query_params = request.query_params.copy()
        query_params_str = str(sorted(query_params.items()))
        return f"companies:{query_params_str}"

    def handle_cached_data(self, cached_data):
        """Handles returning cached data as a response."""
        return Response(cached_data)

    def cache_response(self, cache_key, data):
        """Caches the response data."""
        cache.set(cache_key, data, settings.CACHE_TTL if hasattr(settings, 'CACHE_TTL') else 60)  # Default TTL 60 seconds
```

### Django Celery Integration

Running Celery Beat from the command line within a Django project involves a few key steps, particularly when using django-celery-beat. Here's a breakdown of the process:

Celery and django-celery-beat installed: Ensure you have Celery and the django-celery-beat package installed in your Django project's virtual environment.
Redis (or another broker) running: Your message broker (typically Redis) needs to be up and running.
Django project setup: Your Django project should be properly configured with Celery.

```
celery -A django_companies beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

- `celery`: This invokes the Celery command-line tool.
- `-A django_companies`: This tells Celery where to find your Celery app instance.
- `beat`: This tells Celery to run the Beat scheduler.
- `-l info`: This sets the logging level to "info," so you'll see informative messages about scheduled tasks.
- `--scheduler django_celery_beat.schedulers:DatabaseScheduler`: This is crucial when using `django-celery-beat`. It tells Celery Beat to use the database scheduler provided by `django-celery-beat`, which allows you to manage periodic tasks through the Django admin interface.

### Important considerations

- Worker Running: Remember that Celery Beat only schedules tasks. You also need to have Celery Workers running to actually execute those tasks. To run a worker, you would use a command similar to this:

```
celery -A django_companies worker -l info
```

django-celery-beat database: If you are using django-celery-beat, ensure that you have run the database migrations.

```
python manage.py migrate
```

#### 1. Install Celery and Redis (or another broker)

- Using pip:

```
pip install celery redis django-celery-beat django-redis
```
It assumes you're using Redis as message broker.

#### 2. Create a Celery instance

In your Django project's main app directory (the one containing settings.py), create a file named celery.py:

#### django_companies/celery.py

```Python
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_companies.settings')

app = Celery('django_companies')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

#### 3. Configure Celery by making following changes in settings.py

```
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'  # Or 'amqp://guest:guest@localhost:5672//' for RabbitMQ
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0' # Same as Broker or another redis instance
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC' # Or your desired timezone.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler' # Required for django celery beat.
```

#### 4. Run Redis or RabbitMQ server

Check through the terminal or GUI whether you're configured message broker is running or not.

#### 5. Start the Celery Worker

- Open a terminal and navigate to your project directory.
- Run the following command:

```
celery -A django_companies worker -l info
```

#### 6. Start Celery Beat (for scheduled tasks)

- To schedule tasks, you need to start Celery Beat.
- Open another terminal window and run:

```
celery -A your_project_name beat -l info
```

#### 7. Create tasks for your Django app

Inside companies/tasks.py file

```Python
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def example_task(param1, param2):
    logger.info(f"Executing example_task with {param1}, {param2}")
    result = param1 + param2
    print(f"Example Task Result: {result}")
    return result

```

#### 8. Define Scheduled Tasks inside settings.py file

```Python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'add-every-minute': {
        'task': 'myapp.tasks.example_task',
        'schedule': crontab(minute='*/1'),
        'args': (16, 16)
    },
}
```

#### 9. Run Celery Migrations

- Run database migrations to create the necessary tables for django-celery-beat:
- python manage.py migrate

```
celery -A django_companies beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Running the worker 

```
celery -A django_companies worker -l info
```