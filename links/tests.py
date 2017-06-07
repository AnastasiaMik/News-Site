"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from links.models import Link

class ModelTestCase(TestCase):
    def setUp(self):
        self.link_title = 'Книжный парад'
        self.link = Link(name=self.link_title)

    def test_model_created_link(self):
        old_count = Link.objects.count()
        self.link.save()
        new_count = Link.objects.count()
        self.assertNotEqual(old_count, new_count)
        
