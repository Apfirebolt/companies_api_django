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


