import json
import requests
from requests.exceptions import HTTPError

from schematics.types import IntType
from schematics.types import StringType
from schematics.types import URLType
from schematics.types.compound import ModelType

from alias_app.core.models import RuleCollection as BaseRuleCollection
from alias_app.core.models import Rule as BaseRule


class Rule(BaseRule):
    url = "https://api.alwaysdata.com/v1/mailbox/rule/"

    resource_id = IntType()
    href = URLType()
    alias_id = IntType()
    target = StringType()
    condition = StringType()
    condition_value = StringType()
    action = StringType()
    action_value = StringType()
    collection = ModelType(BaseRuleCollection)

    def __init__(self, alias_id, target, condition, condition_value, *args, **kwargs):
        resource_id = kwargs.pop('resource_id', None)
        href = kwargs.pop('href', None)
        action = kwargs.pop('action', None)
        action_value = kwargs.pop('action_value', None)
        collection = kwargs.pop('collection', None)

        super(Rule, self).__init__(*args, **kwargs)

        self.resource_id = resource_id
        self.href = href
        self.alias_id = alias_id
        self.target = target
        self.condition = condition
        self.condition_value = condition_value
        self.action = action
        self.action_value = action_value
        self.collection = collection

    def __str__(self):
        return "if {} {} {} then {}".format(self.target, self.condition, self.condition_value, self.action)

    def __repr__(self):
        return "Rule #{} on alias #{} ({})".format(self.resource_id, self.alias_id, self.href)

    def save(self):
        self.validate()

        if self.resource_id is None:
            # Create
            data = {
                'mailbox': self.alias_id,
                'target': self.target,
                'condition': self.condition,
                'condition_value': self.condition_value,
                'action': self.action,
                'action_value': self.action_value,
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
                'mailbox': self.alias_id,
                'target': self.target,
                'condition': self.condition,
                'condition_value': self.condition_value,
                'action': self.action,
                'action_value': self.action_value,
            }

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


class RuleCollection(BaseRuleCollection):
    items_class = Rule

    def fetch(self):
        response = requests.get(
            self.items_class.url,
            auth=self.handler.credentials,
        )

        items = []
        for json_rule in response.json():
            rule = Rule(
                resource_id=json_rule['id'],
                href="".join([self.handler.api_url, json_rule['href']]),
                alias_id=int(json_rule['mailbox']['href'].split('/')[-2]),
                target=json_rule['target'],
                condition=json_rule['condition'],
                condition_value=json_rule['condition_value'],
                action=json_rule['action'],
                action_value=json_rule['action_value'],
                collection=self,
            )
            items.append(rule)

        self.items = items
