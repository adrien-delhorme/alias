from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from .forms import SetupForm
from .models import Settings


@sensitive_post_parameters()
@csrf_protect
@never_cache
def home_view(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)

    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }

    return TemplateResponse(request, 'webapp/home.html', context)


def wizard_view(request):
    try:
        settings = request.user.settings
    except ObjectDoesNotExist:
        settings = Settings.objects.create(user=request.user)

    if settings.is_setup_done:
        return redirect('alias-list')
    else:
        return redirect('setup')


@login_required
def setup_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SetupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            hosting_service = form.cleaned_data['hosting_service']
            api_key = form.cleaned_data['api_key']

            settings = request.user.settings
            settings.api_key = api_key
            settings.hosting_service = hosting_service
            settings.is_setup_done = True
            settings.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('alias-list'))

    # if a GET (or any other method) we'll create a blank form
    else:
        settings = request.user.settings

        form = SetupForm(initial={
            'api_key': settings.api_key,
            'hosting_service': settings.hosting_service
        })

    return render(request, 'webapp/setup.html', {'form': form})


@login_required
def alias_list_view(request):
    api_key = request.user.settings.api_key
    hosting_service = request.user.settings.hosting_service

    if hosting_service is None:
        return HttpResponseRedirect(reverse('setup'))
    else:
        module = hosting_service.get_handler()
        handler = module.Handler(credentials=(api_key, ''))
        alias_list = handler.alias.items

        last_used_email = handler.alias.items[-1].redirect_to
        last_used_domain = handler.alias.items[-1].domain_id
        empty_form = handler.form_class(handler, initial={'redirect_to': last_used_email, 'domain_id': last_used_domain}, domains_choices=handler.domains.items, prefix="form-__prefix__")

        if request.method == 'POST':
            alias_forms = []

            for alias in alias_list:
                alias_form = handler.form_class(handler, request.POST, domains_choices=handler.domains.items, prefix=alias.resource_id)
                if alias_form.is_valid():
                    alias_form.save(request)
                    return HttpResponseRedirect(reverse('alias-list'))
                else:
                    alias_form = handler.form_class(handler, initial=alias.to_native(), domains_choices=handler.domains.items, prefix=alias.resource_id)

                alias_forms.append(alias_form)

            empty_form = handler.form_class(handler, request.POST, domains_choices=handler.domains.items, prefix="form-__prefix__")
            if empty_form.is_valid():
                empty_form.save(request)
                return HttpResponseRedirect(reverse('alias-list'))

        else:
            alias_forms = [handler.form_class(handler, initial=alias.to_native(), domains_choices=handler.domains.items, prefix=alias.resource_id) for alias in alias_list]

        data = {
            'hosting_service': hosting_service,
            'alias_forms': alias_forms,
            'empty_form': empty_form,
        }

    return render(request, 'webapp/alias_list.html', data)


@login_required
def alias_delete_view(request, resource_id):
    api_key = request.user.settings.api_key
    hosting_service = request.user.settings.hosting_service

    if hosting_service is None:
        return HttpResponseRedirect(reverse('setup'))
    else:
        module = hosting_service.get_handler()
        handler = module.Handler(credentials=(api_key, ''))

    # Delete alias
    try:
        resource_id = int(resource_id)
    except (ValueError, TypeError):
        return HttpResponseNotFound()

    alias = handler.alias.find('resource_id', resource_id)
    handler.alias.remove('resource_id', resource_id)
    messages.success(request, 'Alias {} has been removed.'.format(alias))

    return HttpResponseRedirect(reverse('alias-list'))
