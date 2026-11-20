from django.db import migrations, models


def create_setup_lock(apps, schema_editor):
    setup_lock = apps.get_model('accounts', 'InitialAdminSetupLock')
    setup_lock.objects.using(schema_editor.connection.alias).get_or_create(pk=1)


def remove_setup_lock(apps, schema_editor):
    setup_lock = apps.get_model('accounts', 'InitialAdminSetupLock')
    setup_lock.objects.using(schema_editor.connection.alias).filter(pk=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_create_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitialAdminSetupLock',
            fields=[
                (
                    'id',
                    models.PositiveSmallIntegerField(
                        default=1,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('revision', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.RunPython(create_setup_lock, remove_setup_lock),
    ]
