# myapp/documents.py (assuming your app is named 'myapp')

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Company  # Import your Company model

@registry.register_document
class CompanyDocument(Document):
    # 1. Define Fields with appropriate Elasticsearch types

    name = fields.TextField(
        attr='name',
        # 'KeywordField' is good for exact matching (e.g., filtering)
        fields={'raw': fields.KeywordField()}
    )
    
    # 'FloatField' is perfect for numerical rating
    rating = fields.FloatField(attr='rating')

    # 'TextField' is ideal for full-text searching (like review content)
    review = fields.TextField(attr='review')

    # 'KeywordField' is better for categorical or exact data (like filters)
    company_type = fields.KeywordField(attr='company_type')
    head_quarters = fields.KeywordField(attr='head_quarters')
    company_age = fields.KeywordField(attr='company_age')
    no_of_employee = fields.KeywordField(attr='no_of_employee')


    # 2. Define the Index and Django Model connection
    class Index:
        name = 'companies' 
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Company 

        fields = [
            'id',
        ]
        