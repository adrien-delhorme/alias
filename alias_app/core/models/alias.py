import re
from django.utils.encoding import python_2_unicode_compatible
from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import BooleanType
from schematics.types import EmailType
from schematics.types import IntType
from schematics.types import StringType
from schematics.types import URLType
from schematics.types.compound import ModelType
from schematics.types.serializable import serializable

from .collection import Collection
from .domain import Domain
from .resource import Resource
from .rule import Rule


def is_email_left_part(value):
    email_re = re.compile(r"^[^\.\\/\(\){}@][^\\/\(\){}@]*$")
    test = email_re.search(value)

    if test is None:
        raise ValidationError(u'Name should not contains accents or /\@(){}')
    return value


@python_2_unicode_compatible
class Alias(Model, Resource):
    resource_id = IntType()
    href = URLType()
    domain = ModelType(Domain)
    name = StringType(validators=[is_email_left_part])
    redirect_to = EmailType()
    is_enabled = BooleanType()
    collection = ModelType(Collection)
    rule = ModelType(Rule)

    @serializable
    def domain_id(self):
        return self.domain.resource_id

    @serializable
    def whitelist(self):
        if hasattr(self.rule, 'condition_value'):
            return self.rule.condition_value

    def __init__(self, name, domain, redirect_to, **kwargs):
        resource_id = kwargs.pop('resource_id', None)
        href = kwargs.pop('href', None)
        is_enabled = kwargs.pop('is_enabled', False)
        collection = kwargs.pop('collection', None)
        rule = kwargs.pop('rule', None)

        super(Alias, self).__init__(**kwargs)

        self.resource_id = resource_id
        self.href = href
        self.domain = domain
        self.name = name
        self.redirect_to = redirect_to
        self.is_enabled = is_enabled
        self.collection = collection
        if rule is not None:
            self.rule = rule

    def __str__(self):
        return "{}@{}".format(self.name, self.domain.name)


class AliasCollection(Collection):
    items_class = Alias
