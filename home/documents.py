from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from product.models import Product


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = Product
        fields = ['name', 'slug']
