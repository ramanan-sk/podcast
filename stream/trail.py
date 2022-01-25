from django.contrib.auth.models import User

user = User.objects.get(pk='ramanan-sk')
user.profile.name = 'Ramanan'
user.save()