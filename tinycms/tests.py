from django.test import TestCase
from django.test.client import Client

from models import *

import datetime

class ModellTest(TestCase):
    def setUp(self):
        pass

    def test_page(self):
        page=Page(slug="test",template="tinycms/test_template.html")
        page.save()
        page2=Page(slug="test2",template="tinycms/test_template.html",parent=page)
        page2.save()


