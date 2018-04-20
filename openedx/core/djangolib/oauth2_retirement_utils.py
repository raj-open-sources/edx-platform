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

def delete_user_from(model, user_id):
    user_query_results = model.objects.filter(user_id=user_id)

    if not user_query_results.exists():
        return False

    user_query_results.delete()
    return True

def delete_from_oauth2_provider_accesstoken(user):
    return delete_user_from(model=DOTAccessToken, user_id=user.id)

def delete_from_oauth2_provider_application(user):
    return delete_user_from(model=DOTApplication, user_id=user.id)

def delete_from_oauth2_provider_grant(user):
    return delete_user_from(model=DOTGrant, user_id=user.id)

def delete_from_oauth2_provider_refreshtoken(user):
    return delete_user_from(model=DOTRefreshToken, user_id=user.id)

def delete_from_oauth2_accesstoken(user):
    return delete_user_from(model=DOPAccessToken, user_id=user.id)

def delete_from_oauth2_refreshtoken(user):
    return delete_user_from(model=DOPRefreshToken, user_id=user.id)

def delete_from_oauth2_grant(user):
    return delete_user_from(model=DOPGrant, user_id=user.id)