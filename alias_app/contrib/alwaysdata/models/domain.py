import requests

from schematics.types import IntType
from schematics.types import StringType
from schematics.types import URLType

from alias_app.core.models import DomainCollection as BaseDomainCollection
from alias_app.core.models import Domain as BaseDomain


class Domain(BaseDomain):
    url = "https://api.alwaysdata.com/v1/domain/"

    resource_id = IntType()
    href = URLType()
    name = StringType()

    def __init__(self, resource_id, href, name, collection, *args, **kwargs):
        super(Domain, self).__init__(*args, **kwargs)
        self.resource_id = resource_id
        self.href = href
        self.name = name
        self.collection = collection

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{} ({})".format(self.name, self.href)


class DomainCollection(BaseDomainCollection):
    items_class = Domain

    def fetch(self):
        response = requests.get(
            self.items_class.url,
            auth=self.handler.credentials,
        )

        items = []
        for json_domains in response.json():
            domain = Domain(
                resource_id=json_domains['id'],
                href="".join([self.handler.api_url, json_domains['href']]),
                name=json_domains['name'],
                collection=self,
            )
            items.append(domain)
        self.items = items
