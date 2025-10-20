from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from core.models import Company  # Assuming your app name is 'core'

@registry.register_document
class CompanyDocument(Document):

    employee_count = fields.KeywordField(
        attr='no_of_employee',
        # This will be used for filtering/faceting
    )

    age = fields.KeywordField() # The Elasticsearch field name is 'age'

    def prepare_age(self, instance):
        """
        Cleans and normalizes the 'company_age' field for indexing.
        Example: "10 years old" -> "10 years"
        """
        age_str = instance.company_age
        if age_str and " years old" in age_str:
            return age_str.replace(" years old", " years").strip()
        return age_str
    
    # ----------------------------------------------------------------------
    # Regular Field Definitions (for text search/sorting)
    # ----------------------------------------------------------------------
    
    name = fields.TextField(
        analyzer='standard',
        fields={
            'suggest': fields.CompletionField(), # For autocomplete features
            'keyword': fields.KeywordField(),    # For exact matching
        }
    )

    rating = fields.FloatField()
    
    review = fields.TextField(analyzer='standard')

    # Using KeywordField for filtering on specific company types
    company_type = fields.KeywordField()

    head_quarters = fields.KeywordField() # For filtering by city/location

    class Index:
        # Define the name of the Elasticsearch index
        name = 'companies'
        # Define index settings
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Company  # The Django model to index
        
        # List all Django fields NOT explicitly defined above for automatic mapping.
        # Since we defined most fields manually, we can omit 'fields' here or 
        # list the remaining model fields if you want them indexed automatically.
        # In this example, we've defined all relevant fields explicitly.
        pass