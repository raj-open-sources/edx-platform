from oauth2_provider.models import (
    AccessToken as DOTAccessToken,
    Application as DOTApplication,
    Grant as DOTGrant,
    RefreshToken as DOTRefreshToken,
)
from provider.oauth2.models import (
    AccessToken as DOPAccessToken,
    RefreshToken as DOPRefreshToken,
    Grant as DOPGrant,
)


class OAuth2Retirer(object):

    def __init__(self, models_to_retire):
        self._models_to_retire = models_to_retire

    def retire_user(self, user):
        for model in self._models_to_retire:
            self._delete_user_from(model=model, user_id=user)

    def _delete_user_from(self, model, user_id):
        user_query_results = model.objects.filter(user_id=user_id)

        if not user_query_results.exists():
            return False

        user_query_results.delete()
        return True


def retire_dot_oauth2_models(user):
    dot_models = [DOTAccessToken, DOTApplication, DOTGrant, DOTRefreshToken]
    OAuth2Retirer(dot_models).retire_user(user)


def retire_dop_oauth2_models(user):
    dop_models = [DOPAccessToken, DOPGrant, DOPRefreshToken]
    OAuth2Retirer(dop_models).retire_user(user)
