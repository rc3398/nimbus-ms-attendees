import json, jwt, requests
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

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


    def jwt_decode_token(token):
        header = jwt.get_unverified_header(token)
        jwks = requests.get('https://{}/.well-known/jwks.json'.format(
            settings.AUTH0_DOMAIN
        )).json()

        public_key = None
        for jwk in jwks['keys']:
            if jwk['kid'] == header['kid']:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

        if public_key is None:
            raise Exception('Public key not found.')

        issuer = 'https://{}/'.format(settings.AUTH0_DOMAIN)
        payload = jwt.decode(
            token,
            public_key,
            audience=settings.AUTH0_AUDIENCE,
            issuer=issuer,
            algorithms=['RS256']
        )
        return payload


    def parse_from_token(token):
        return ""

'''
Documentation
- https://developers.google.com/identity/openid-connect/openid-connect#server-flow

'''