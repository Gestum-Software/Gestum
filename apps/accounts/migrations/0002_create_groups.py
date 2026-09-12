from django.db import migrations


def create_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")

    usuario, _ = Group.objects.get_or_create(name="usuario")
    tecnico, _ = Group.objects.get_or_create(name="tecnico")
    admin, _ = Group.objects.get_or_create(name="admin")

    resource_content_type, _ = ContentType.objects.get_or_create(
        app_label="resources",
        model="resource",
    )

    def get_permission(codename, name):
        permission, _ = Permission.objects.get_or_create(
            content_type=resource_content_type,
            codename=codename,
            defaults={"name": name},
        )
        return permission

    # Permissões nativas do model Resource
    add_resource = get_permission("add_resource", "Can add resource")
    change_resource = get_permission("change_resource", "Can change resource")
    delete_resource = get_permission("delete_resource", "Can delete resource")
    view_resource = get_permission("view_resource", "Can view resource")

    # Usuário
    usuario.permissions.add(view_resource)

    # Técnico
    tecnico.permissions.add(
        view_resource,
        add_resource,
        change_resource,
    )

    # Administrador
    admin.permissions.add(
        view_resource,
        add_resource,
        change_resource,
        delete_resource,
    )


def remove_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    Group.objects.filter(
        name__in=["usuario", "tecnico", "admin"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("resources", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_groups_and_permissions,
            remove_groups_and_permissions,
        ),
    ]
