from django import template
from django.core.urlresolvers import reverse


register = template.Library()

@register.simple_tag
def api_detail(resource_name, pk):
    """Return API URL for Tastypie Resource details.

    Usage::

        {% api_detail 'entry' entry.pk %}

    or::

        {% api_detail 'api2:entry' entry.pk %}
    """
    if ':' in resource_name:
        api_name, resource_name = resource_name.split(':', 1)
    else:
        api_name = 'v1'
    return reverse('api_dispatch_detail', kwargs={
        'api_name': api_name,
        'resource_name': resource_name,
        'pk': pk
    }) + '?format=json'


@register.simple_tag
def api_list(resource_name):
    """Return API URL for Tastypie Resource list.

    Usage::

        {% api_list 'entry' %}

    or::

        {% api_list 'api2:entry' %}
    """
    if ':' in resource_name:
        api_name, resource_name = resource_name.split(':', 1)
    else:
        api_name = 'v1'
    return reverse('api_dispatch_list', kwargs={
        'api_name': api_name,
        'resource_name': resource_name,
    }) + '?format=json'