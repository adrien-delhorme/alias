from django.contrib import messages
from alias_app.core.forms import AliasForm
from .models.alias import Alias
from .models.rule import Rule


class AlwaysdataAliasForm(AliasForm):
    def save(self, request):
        data = self.cleaned_data
        resource_id = data.get('resource_id', None)

        domain = self.handler.domains.find('resource_id', data['domain_id'])
        whitelist = data.get('whitelist', '')

        if resource_id is not None:
            # Update Alias
            alias = self.handler.alias.find('resource_id', data['resource_id'])
            alias.name = data['name']
            alias.domain = domain
            alias.redirect_to = data['redirect_to']
            alias.is_enabled = data['is_enabled']
            alias.save()

            if whitelist != '':
                if alias.rule is not None:
                    # Update rule
                    rule = self.handler.rules.find('resource_id', alias.rule.resource_id)
                    rule.condition_value = whitelist
                    rule.save()
                    alias.rule = rule
                else:
                    self.create_rule(alias, whitelist)
            else:
                if alias.rule is not None:
                    # Delete rule
                    rule = self.handler.rules.find('resource_id', alias.rule.resource_id)
                    self.handler.rules.remove('resource_id', rule.resource_id)
                    alias.rule = None

            alias.save()
            messages.success(request, 'Alias {} has been updated.'.format(alias))

            if "send_test" in data and data['send_test'] is True:
                # Send a test email
                self.send_test_email(str(alias))
                messages.success(request, 'A test e-mail has been sent to {}.'.format(alias))

        else:
            # Create Alias
            alias = Alias(
                data['name'],
                domain,
                data['redirect_to'],
                is_enabled=True,
                collection=self.handler.alias,
            )
            self.handler.alias.add(alias)

            # Save the alias to get its resource_id (required to create a rule object)
            alias.save()

            if whitelist != '':
                self.create_rule(alias, whitelist)
                alias.save()

            messages.success(request, 'Alias {} has been created.'.format(alias))

    def create_rule(self, alias, whitelist):
        rule = Rule(
            alias_id=alias.resource_id,
            target='FROM',
            condition='CONTAINS',
            condition_value=whitelist,
            action='DISCARD',
            collection=self.handler.rules,
        )
        rule.save()
        alias.rule = rule
        self.handler.rules.add(rule)
