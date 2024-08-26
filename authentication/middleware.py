from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from accounts.models import User
import jwt
from channels.middleware import BaseMiddleware

from windam_backend import settings

@database_sync_to_async
def get_user(token_key):
    try:
        decoded = jwt.decode(token_key, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(pk=decoded['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        return AnonymousUser()
    except User.DoesNotExist:
        return AnonymousUser()
    except jwt.InvalidTokenError:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token_key = None
        if b'authorization' in headers:
            try:
                scheme, token_key = headers[b'authorization'].decode().split()
                if scheme.lower() != 'bearer':
                    raise ValueError("Invalid authorization scheme")
            except (ValueError, IndexError):
                # Log the invalid token or scheme
                scope['user'] = AnonymousUser()
                return await self.inner(scope, receive, send)
       
        query_string = parse_qs(scope['query_string'].decode())
        token_key = query_string.get('token', [None])[0]
        print('token_key', token_key)
        if token_key is None:
            raise ValueError("No token provided")
        else:
            user = await get_user(token_key)
            scope['user'] = user
            if user is AnonymousUser():
                raise ValueError("Invalid token")

        return await super().__call__(scope, receive, send)

