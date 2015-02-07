from schematics.models import Model
from schematics.types.compound import ModelType

from .collection import Collection
from .resource import Resource


class Rule(Model, Resource):
    collection = ModelType(Collection)


class RuleCollection(Collection):
    items_class = Rule
