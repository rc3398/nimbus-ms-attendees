import json, jwt, requests

class NimbusJWT_Authentication(access_token):
    def authenticate(self, request):
        res = super().authenticate(request)
        if res is None:
            return res

        user, token = res
        if not user.email:
            user_info = requests.get(
                f'https://{settings.AUTH0_DOMAIN}/userinfo',
                headers={'Authorization': f'Bearer {token}'}
            ).json()

            if not user_info.get('email_verified'):
                raise AuthenticationFailed(
                    'You must verify your email before using this service.'
                )
            user.email = user_info.get('email')
            user.save()
        return user, token

'''
Documentation
- https://developers.google.com/identity/openid-connect/openid-connect#server-flow

'''