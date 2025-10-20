from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from .serializers import (
    ListCustomUserSerializer,
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    CompanySerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from django.core.cache import cache
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import CustomUser
from core.models import Company
from core.documents import CompanyDocument
from elasticsearch_dsl import Q
from rest_framework.response import Response
from .pagination import CustomPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ViewSet


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")

        if CustomUser.objects.filter(username=username).exists():
            return Response({"message": "Username already exists"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"message": "Email already exists"}, status=400)

        return super().post(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["username", "email"]
    ordering_fields = ["username", "email"]
    search_fields = ["username", "email"]


class UserProfileApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ListCompaniesApiView(ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = [
        "name",
        "head_quarters",
    ]
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
        cache.set(
            cache_key,
            data,
            settings.CACHE_TTL if hasattr(settings, "CACHE_TTL") else 60,
        )  # Default TTL 60 seconds


@api_view(["GET"])
@permission_classes([])
def get_companies(request):

    s = CompanyDocument.search()
    
    # Get the search query from the request's query parameters
    query = request.query_params.get('q', None)
    
    if query:
        search_fields = ['name', 'review', 'company_type']
        
        q = Q(
            'multi_match', 
            query=query, 
            fields=search_fields, 
            fuzziness='AUTO' # Optional: Add fuzzy matching for better results
        )
        s = s.query(q)
    try:
        companies_queryset = s.to_queryset()
    except Exception as e:
        # Handle connection errors or other ES issues gracefully
        print(f"Elasticsearch Error: {e}")
        return Response({"detail": "Search service temporarily unavailable."}, status=503)

    serializer = CompanySerializer(companies_queryset, many=True)
    return Response(serializer.data)


class CompanyViewSet(ViewSet):
    permission_classes = []
    pagination_class = CustomPagination

    def list(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        company = Company.objects.get(id=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)
