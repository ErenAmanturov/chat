from channels.middleware import BaseMiddleware

from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.tokens import AccessToken

from urllib.parse import parse_qs

import jwt


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get('token', [None])[0]

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                user = await self.get_user(user_id)
                scope['user'] = user
            except jwt.InvalidTokenError:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
    
    async def get_user(self, user_id):
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            return await User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
