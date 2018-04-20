import datetime
from uuid import uuid4

from django.test import TestCase
from openedx.core.djangoapps.oauth_dispatch.tests import factories
from student.tests.factories import UserFactory
from oauth2_provider.models import (
    AccessToken as DOTAccessToken,
    Application as DOTApplication,
    RefreshToken as DOTRefreshToken,
    Grant as DOTGrant,
)
from provider.oauth2.models import (
    AccessToken as DOPAccessToken,
    RefreshToken as DOPRefreshToken,
    Grant as DOPGrant,
    Client as DOPClient,
)

from ..oauth2_retirement_utils import (
    delete_from_oauth2_provider_accesstoken,
    delete_from_oauth2_provider_application,
    delete_from_oauth2_provider_grant,
    delete_from_oauth2_provider_refreshtoken,
    delete_from_oauth2_accesstoken,
    delete_from_oauth2_refreshtoken,
    delete_from_oauth2_grant,
)

class TestRetireOAuth2DOT(TestCase):

    def setUp(self):
        super(TestRetireOAuth2DOT, self).setUp()
        self.user = UserFactory.create()
        self.app = factories.ApplicationFactory(user=self.user)

    def test_delete_from_oauth2_provider_application(self):
        delete_from_oauth2_provider_application(self.user)
        applications = DOTApplication.objects.filter(user_id=self.user.id)
        self.assertFalse(applications.exists())

    def test_delete_from_oauth2_provider_accesstoken(self):
        factories.AccessTokenFactory(
            user=self.user,
            application=self.app
        )
        delete_from_oauth2_provider_accesstoken(self.user)
        access_tokens = DOTAccessToken.objects.filter(user_id=self.user.id)
        self.assertFalse(access_tokens.exists())

    def test_delete_from_oauth2_provider_refreshtoken(self):
        access_token = factories.AccessTokenFactory(
            user=self.user,
            application=self.app,
        )
        factories.RefreshTokenFactory(
            user=self.user,
            application=self.app,
            access_token=access_token,
        )
        delete_from_oauth2_provider_refreshtoken(self.user)
        refresh_tokens = DOTRefreshToken.objects.filter(user_id=self.user.id)
        self.assertFalse(refresh_tokens.exists())

    def test_delete_from_oauth2_provider_grant(self):
        DOTGrant.objects.create(
            user=self.user,
            application=self.app,
            expires=datetime.datetime(2018, 1, 1),
        )
        delete_from_oauth2_provider_grant(self.user)
        grants = DOTGrant.objects.filter(
            user=self.user,
        )
        self.assertFalse(grants.exists())


class TestRetireOAuth2DOP(TestCase):

    def setUp(self):
        super(TestRetireOAuth2DOP, self).setUp()
        self.user = UserFactory.create()
        self.client = DOPClient.objects.create(
            user=self.user,
            client_type=1,
        )

    def test_delete_from_oauth2_accesstoken(self):
        DOPAccessToken.objects.create(
            user=self.user,
            client=self.client,
        )
        delete_from_oauth2_accesstoken(self.user)
        access_tokens = DOPAccessToken.objects.filter(
            user=self.user
        )
        self.assertFalse(access_tokens.exists())

    def test_delete_from_oauth2_refreshtoken(self):
        access_token = DOPAccessToken.objects.create(
            user=self.user,
            client=self.client,
        )
        DOPRefreshToken.objects.create(
            user=self.user,
            client=self.client,
            access_token=access_token,
        )
        delete_from_oauth2_refreshtoken(self.user)
        refresh_tokens = DOPRefreshToken.objects.filter(
            user=self.user,
        )
        self.assertFalse(refresh_tokens.exists())

    def test_delete_from_oauth2_grant(self):
        DOPGrant.objects.create(
            user_id=self.user.id,
            client_id=self.client.id,
        )
        delete_from_oauth2_grant(self.user)
        grants = DOPGrant.objects.filter(
            user_id=self.user.id
        )
        self.assertFalse(grants.exists())
