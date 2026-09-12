from django.db import migrations


def create_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    usuario, _ = Group.objects.get_or_create(name="usuario")
    tecnico, _ = Group.objects.get_or_create(name="tecnico")
    admin, _ = Group.objects.get_or_create(name="admin")

    def get_permission(app_label, model, codename):
        return Permission.objects.get(
            content_type__app_label=app_label,
            content_type__model=model,
            codename=codename,
        )

    # Permissões nativas do model Resource
    view_resource = get_permission(
        "resources",
        "resource",
        "view_resource",
    )

    add_resource = get_permission(
        "resources",
        "resource",
        "add_resource",
    )

    change_resource = get_permission(
        "resources",
        "resource",
        "change_resource",
    )

    delete_resource = get_permission(
        "resources",
        "resource",
        "delete_resource",
    )

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
