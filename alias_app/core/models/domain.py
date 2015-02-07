from schematics.models import Model
from schematics.types.compound import ModelType

from .collection import Collection
from .resource import Resource


class Domain(Model, Resource):
    collection = ModelType(Collection)


class DomainCollection(Collection):
    items_class = Domain
