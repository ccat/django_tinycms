from django import template
from django_tinycms.models import *

register = template.Library()

"""
@register.tag(name="show_absolute_menu")
def show_absolute_menu(parser, token):
    Page.objects.root_nodes()


class TinycmsMenuAbsolute(template.Node):
    def render(self):
        pass
"""


@register.simple_tag(takes_context=True)
def show_contents(context, value_name,contentTag=None,titleTag=None):
    if(isinstance(value_name, list)):
        valList = value_name
    else:
        valList = context[value_name]

    result =""

    for item in valList:
        if(titleTag):
            result += "<%s>%s</%s>" % (titleTag,item.title,titleTag)
        if(contentTag):
            result += "<%s>%s</%s>" % (contentTag,item.content,contentTag)
        else:
            result += "%s" % item.content
    return result


