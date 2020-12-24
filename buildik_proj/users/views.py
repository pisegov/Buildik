from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.models import User

@api_view()
@permission_classes([permissions.IsAuthenticated])
def get_user(request):
    jsoned_user = {field.name: getattr(request.user, field.name) for field in User._meta.fields}
    jsoned_user.pop('password')
    return Response(jsoned_user)