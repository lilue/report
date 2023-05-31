from django.test import TestCase

from authorization.models import User


# Create your tests here.

class TestUser(TestCase):
    openid = 'obrbB4qShJ3LHypXLEUbK8dJHzho'
    user = User.objects.get(open_id=openid)
    print(user.to_dict())
