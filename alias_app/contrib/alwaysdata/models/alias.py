import string
import random
import json
import requests
from requests.exceptions import HTTPError
from alias_app.core.models import Alias as BaseAlias
from alias_app.core.models import AliasCollection as BaseAliasCollection


class Alias(BaseAlias):
    url = "https://api.alwaysdata.com/v1/mailbox/"

    def save(self, *args, **kwargs):
        self.validate()

        if self.resource_id is None:
            # Create
            data = {
                'domain': self.domain.resource_id,
                'name': self.name,
                'password': ''.join(random.choice(string.lowercase) for i in range(10)),
                'redirect_enabled': self.is_enabled,
                'redirect_to': self.redirect_to,
            }
            response = requests.post(
                self.url,
                auth=self.collection.handler.credentials,
                data=json.dumps(data)
            )

            if str(response.status_code)[0] != '2':
                raise HTTPError(" ".join([str(response.status_code), response.reason, response.content]))

            # Get the newly created resource_id and href
            self.href = response.headers['location']
            self.resource_id = self.href.split('/')[-2]

        else:
            # Update
            data = {
                'domain': self.domain.resource_id,
                'name': self.name,
                'redirect_enabled': self.is_enabled,
                'redirect_to': self.redirect_to,
            }

            # Need to update rule too
            response = requests.patch(
                "{}{}/".format(self.url, self.resource_id),
                auth=self.collection.handler.credentials,
                data=json.dumps(data),
            )

            if str(response.status_code)[0] != '2':
                raise HTTPError("{} {}".format(response.status_code, response.reason))

    def delete(self):
        if self.resource_id is not None:
            return requests.delete(
                "{}{}/".format(self.url, self.resource_id),
                auth=self.collection.handler.credentials,
            )


class AliasCollection(BaseAliasCollection):
    items_class = Alias

    def fetch(self):
        response = requests.get(
            self.items_class.url,
            auth=self.handler.credentials,
        )

        items = []
        for json_alias in response.json():
            domain = self.handler.domains.find('href', "".join([self.handler.api_url, json_alias['domain']['href']]))
            if domain is not None:
                alias = Alias(
                    resource_id=json_alias['id'],
                    href="".join([self.handler.api_url, json_alias['href']]),
                    domain=domain,
                    name=json_alias['name'],
                    redirect_to=json_alias['redirect_to'],
                    is_enabled=json_alias['redirect_enabled'],
                    collection=self,
                    rule=self.handler.rules.find('alias_id', json_alias['id'])
                )
                items.append(alias)

        self.items = items
