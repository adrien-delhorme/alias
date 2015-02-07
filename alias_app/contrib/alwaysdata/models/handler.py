from schematics.types.compound import ModelType

from alias_app.core.models import Handler as BaseHandler
from alias_app.contrib.alwaysdata.forms import AlwaysdataAliasForm
import alias
import domain
import rule


class Handler(BaseHandler):
    api_url = "https://api.alwaysdata.com"
    alias = ModelType(alias.AliasCollection)
    domains = ModelType(domain.DomainCollection)
    rules = ModelType(rule.RuleCollection)

    form_class = AlwaysdataAliasForm

    def __init__(self, credentials, *args, **kwargs):
        super(Handler, self).__init__(credentials, *args, **kwargs)
        self.domains = domain.DomainCollection(self)
        self.alias = alias.AliasCollection(self)
        self.rules = rule.RuleCollection(self)
        self.credentials = credentials
