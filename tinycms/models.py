from django.db import models
from django.utils import translation
from django.conf import settings
from django.http import Http404#,HttpResponse
#from django.template import Context, Template
from django.shortcuts import render
#from django.shortcuts import render_to_response

from mptt.models import MPTTModel, TreeForeignKey

from views import *

try:
    LANGUAGES = settings.LANGUAGES
except:
    LANGUAGES = ((settings.LANGUAGE_CODE,settings.LANGUAGE_CODE),)

try:
    TEMPLATES = settings.TINYCMS_TEMPLATES
except:
    TEMPLATES = (("tinycms/test_template.html","test_template"),)


class Page(MPTTModel):
    slug = models.CharField(max_length=512)
    template = models.CharField(max_length=1024,choices=TEMPLATES)
    url_overwrite = models.URLField(max_length=2048, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['slug']

    def __unicode__(self):
        return self.slug

    def get_url(self):
        if(self.url_overwrite != None and self.url_overwrite != "" ):
            return self.url_overwrite
        else:
            tempurl = ""
            if(self.parent):
                tempurl = self.parent.get_url()
            tempurl += self.slug+"/"
            return tempurl

    def render(self,request,dics={}):
        tempDic = {}
        for key,val in dics.items():
            tempDic[key] = val
        if(not self.is_active):
            raise Http404
        lang = translation.get_language()
        contents = Content.objects.filter(page=self,language=lang)
        for item in contents:
            if(item.value_name not in tempDic):
                tempDic[item.value_name] = []
            tempDic[item.value_name].append(item.content)
        return render(request, self.template, tempDic)

    def save(self):
        super(Page,self).save()
        Dispatcher.register()

class Content(models.Model):
    #title = models.CharField(max_length=1024)
    page = models.ForeignKey('Page', related_name='contents')
    value_name = models.CharField(max_length=256)
    language = models.CharField(max_length=256, choices=LANGUAGES)
    content = models.TextField()

    def __unicode__(self):
        return unicode(self.title)+":"+unicode(self.language)

    def render(self):
        return self.content

