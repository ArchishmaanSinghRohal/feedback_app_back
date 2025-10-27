# feedback/migrations/000X_create_superuser.py

from django.db import migrations
import os
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()

    DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME')
    DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL') # Optional: Add email if desired
    DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD')

    if not User.objects.filter(username=DJANGO_SU_NAME).exists():
        if DJANGO_SU_NAME and DJANGO_SU_PASSWORD: # Check if variables exist
            print(f'\nCreating superuser: {DJANGO_SU_NAME}')
            User.objects.create_superuser(
                username=DJANGO_SU_NAME,
                email=DJANGO_SU_EMAIL, # Use None if not providing email
                password=DJANGO_SU_PASSWORD
            )
        else:
            print('\nSuperuser creation skipped: Environment variables DJANGO_SU_NAME and DJANGO_SU_PASSWORD not set.')
    else:
        print(f'\nSuperuser {DJANGO_SU_NAME} already exists.')

# We add an empty reverse function because this operation isn't easily reversible
def remove_superuser(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        # Add the previous migration dependency for your app, e.g.:
        ('feedback', '0001_initial'), 
        # OR if adding to 'auth' app (less common):
        # migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_superuser, reverse_code=remove_superuser),
    ]