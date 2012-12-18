# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.test import TestCase
from simplespamblocker import settings as app_settings


DEFAULT_PROFILES = (
    (r'^/comments/post/$', {
        'method': 'post',
        'author': lambda request: request.POST.get('name', ''),
        'email': lambda request: request.POST.get('email', ''),
        'url': lambda request: request.POST.get('url', ''),
        'content': lambda request: request.POST.get('comment', ''),
    }),
)

DEFAULT_PROFILES_WITHOUT_METHOD = (
    (r'^/comments/post/$', {
        'author': lambda request: request.POST.get('name', ''),
        'email': lambda request: request.POST.get('email', ''),
        'url': lambda request: request.POST.get('url', ''),
        'content': lambda request: request.POST.get('comment', ''),
    }),
)


def create_user():
    from django.contrib.auth.models import User
    # comaptible under django 1.3
    return User.objects.create_user('dummyuser', 'dummyuser@example.com', password='test')


class BlockMiddlewareTestCase(TestCase):
    urls = 'simplespamblocker.tests.urls'

    def setUp(self):
        from django.contrib.sites.models import Site
        from django.core.cache import cache
        from simplespamblocker.models import Option
        Option.objects.all().delete()
        self.option = Option.objects.create(site=Site.objects.get_current())
        self.user = create_user()
        # clear regex cache
        cache.clear()

    def _update_option(self, **data):
        for k, v in data.items():
            setattr(self.option, k, v)
        self.option.save()

    def _post_comment(self, **modify_data):
        # this is invalid comment data
        # without security hash, etc...
        data = {
            'name': 'Spammer',
            'email': 'spamham@example.com',
            'url': 'http://spam.example.com/',
            'comment': u'spam spam spam'
        }
        data.update(modify_data)
        return self.client.post('/comments/post/', data)


class BlockMiddlewareValidProfileTests(BlockMiddlewareTestCase):

    def setUp(self):
        # compatible under django 1.3
        self.old_settings = getattr(settings, 'SIMPLESPAMBLOCKER_PROFILES', [])
        settings.SIMPLESPAMBLOCKER_PROFILES = DEFAULT_PROFILES
        super(BlockMiddlewareValidProfileTests, self).setUp()

    def tearDown(self):
        settings.SIMPLESPAMBLOCKER_PROFILES = self.old_settings

    def test_it_author(self):
        self._update_option(block_author='spammer|hammer')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)

    def test_it_content(self):
        self._update_option(block_content='^(spam\s?)+$')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)

    def test_it_email(self):
        self._update_option(block_email='^.*@example.com$')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)

    def test_it_remote_addr(self):
        self._update_option(block_remote_addr='127.0.0.1')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)

    def test_it_url(self):
        self._update_option(block_url='spam')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)

    def test_it_referer(self):
        self._update_option(block_http_referer='evil')
        self.client.defaults.update(HTTP_REFERER='http://external.example.com/evil/')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)

    def test_it_empty_referer(self):
        self._update_option(block_http_referer='^$')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)

    def test_it_user_agent(self):
        self._update_option(block_http_user_agent='googlebot')
        self.client.defaults.update(
            HTTP_USER_AGENT='Googlebot/2.1 (+http://www.google.com/bot.html)')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)

    def test_it_non_option(self):
        res = self._post_comment()
        self.assertEqual(res.status_code, 400)  # Comment Bad Request

    def test_response_content(self):
        """ render default message
        """
        self._update_option(block_remote_addr='127.0.0.1')
        res = self._post_comment()
        self.assertContains(res, 'Your comment was detected as a SPAM', status_code=403)

    def test_it_method(self):
        """ blocked only method on profile
        """
        self._update_option(block_remote_addr='127.0.0.1')
        res = self._post_comment()
        self.assertContains(res, 'Your comment was detected as a SPAM', status_code=403)
        # through middleware when different method
        res = self.client.get('/comments/post/')
        self.assertEqual(res.status_code, 405)  # returned comment views


class BlockMiddlewareEmptyProfileTests(BlockMiddlewareTestCase):

    def setUp(self):
        # compatible under django 1.3
        self.old_settings = getattr(settings, 'SIMPLESPAMBLOCKER_PROFILES', [])
        settings.SIMPLESPAMBLOCKER_PROFILES = []
        super(BlockMiddlewareEmptyProfileTests, self).setUp()

    def tearDown(self):
        settings.SIMPLESPAMBLOCKER_PROFILES = self.old_settings

    def test_it_non_settings(self):
        self._update_option(block_remote_addr='127.0.0.1')
        res = self._post_comment()
        self.assertEqual(res.status_code, 400)  # Comment Bad Request


class BlockMiddlewareNonMethodProfileTests(BlockMiddlewareTestCase):

    def setUp(self):
        # compatible under django 1.3
        self.old_settings = getattr(settings, 'SIMPLESPAMBLOCKER_PROFILES', [])
        settings.SIMPLESPAMBLOCKER_PROFILES = DEFAULT_PROFILES_WITHOUT_METHOD
        super(BlockMiddlewareNonMethodProfileTests, self).setUp()

    def tearDown(self):
        settings.SIMPLESPAMBLOCKER_PROFILES = self.old_settings

    def test_it(self):
        """ all request become target
        """
        self._update_option(block_remote_addr='127.0.0.1')
        res = self._post_comment()
        self.assertEqual(res.status_code, 403)
        res = self.client.get('/comments/post/')
        self.assertEqual(res.status_code, 403)


class BlockMiddlewareWithTemplateTests(BlockMiddlewareTestCase):

    def setUp(self):
        # compatible under django 1.3
        self.old_SIMPLESPAMBLOCKER_PROFILES = getattr(
            settings, 'SIMPLESPAMBLOCKER_PROFILES', [])
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.SIMPLESPAMBLOCKER_PROFILES = DEFAULT_PROFILES
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS + (
            os.path.join(os.path.dirname(__file__), 'templates'),
        )
        self.old_SPAM_TEMPLATE = app_settings.SPAM_TEMPLATE
        app_settings.SPAM_TEMPLATE = 'simplespamblocker/blocked.html'
        super(BlockMiddlewareWithTemplateTests, self).setUp()

    def tearDown(self):
        settings.SIMPLESPAMBLOCKER_PROFILES = self.old_SIMPLESPAMBLOCKER_PROFILES
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS
        app_settings.SPAM_TEMPLATE = self.old_TEMPLATE_DIRS

    def test_it(self):
        """ render custom template
        """
        self._update_option(block_remote_addr='127.0.0.1')
        res = self._post_comment()
        self.assertContains(res, 'You are Spam!', status_code=403)
