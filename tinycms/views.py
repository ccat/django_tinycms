
from django.http import Http404

from models import *

class Dispatcher(object):

    dispatchURLs = None

    @classmethod
    def dispatch(cls,url,request):
        if(cls.dispatchURLs==None):
            cls.register()
        if(url in cls.dispatchURLs):
            return cls.dispatchURLs[url].render(request)
        raise Http404

    @classmethod
    def register(cls):
        cls.dispatchURLs={}
        page_roots = Page.objects.root_nodes()

        for item in page_roots:
            cls.generate_url(item)

    @classmethod
    def generate_url(cls,node):
        if(node.is_active):
            cls.dispatchURLs[node.get_url()]=node
            for item in node.get_children():
                cls.generate_url(item)

def show_page(request,url):
    return Dispatcher.dispatch(url,request)
    #return page.render(request)



"""
from models import *
def generate_url(node):
    urlpatterns = patterns("")
    if(node.is_active):
        urlpatterns += patterns('',url("^"+node.get_url()+"$","django_tinycms.views.show_page",{"page":node}))
    for item in node.get_children():
        urlpatterns += generate_url(item)
    return urlpatterns


urlpatterns = patterns("")
page_roots = Page.objects.root_nodes()

for item in page_roots:
    urlpatterns += generate_url(item)
"""


