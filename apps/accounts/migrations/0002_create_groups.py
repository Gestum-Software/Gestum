from django.db import migrations


def create_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")

    usuario, _ = Group.objects.get_or_create(name="usuario")
    tecnico, _ = Group.objects.get_or_create(name="tecnico")
    admin, _ = Group.objects.get_or_create(name="admin")

    def get_content_type(app_label, model):
        content_type, _ = ContentType.objects.get_or_create(
            app_label=app_label,
            model=model,
        )
        return content_type

    resource_content_type = get_content_type("resources", "resource")
    ticket_content_type = get_content_type("tickets", "ticket")
    user_content_type = get_content_type("accounts", "customuser")
    reservation_content_type = get_content_type(
        "reservations", "reservation"
    )

    def get_permission(content_type, codename, name):
        permission, _ = Permission.objects.get_or_create(
            content_type=content_type,
            codename=codename,
            defaults={"name": name},
        )
        return permission

    # Permissões nativas do model Resource
    add_resource = get_permission(
        resource_content_type, "add_resource", "Can add resource"
    )
    change_resource = get_permission(
        resource_content_type, "change_resource", "Can change resource"
    )
    delete_resource = get_permission(
        resource_content_type, "delete_resource", "Can delete resource"
    )
    view_resource = get_permission(
        resource_content_type, "view_resource", "Can view resource"
    )

    # Permissões nativas do model Ticket
    add_ticket = get_permission(
        ticket_content_type, "add_ticket", "Can add ticket"
    )
    change_ticket = get_permission(
        ticket_content_type, "change_ticket", "Can change ticket"
    )
    delete_ticket = get_permission(
        ticket_content_type, "delete_ticket", "Can delete ticket"
    )
    view_ticket = get_permission(
        ticket_content_type, "view_ticket", "Can view ticket"
    )

    # Permissões nativas do model Custom User
    add_customuser = get_permission(
        user_content_type, "add_customuser", "Can add customuser"
    )
    change_customuser = get_permission(
        user_content_type, "change_customuser", "Can change customuser"
    )
    delete_customuser = get_permission(
        user_content_type, "delete_customuser", "Can delete customuser"
    )
    view_customuser = get_permission(
        user_content_type, "view_customuser", "Can view customuser"
    )

    # Permissões nativas do model Reservation
    add_reservation = get_permission(
        reservation_content_type, "add_reservation", "Can add reservation"
    )
    change_reservation = get_permission(
        reservation_content_type, "change_reservation", "Can change reservation"
    )
    delete_reservation = get_permission(
        reservation_content_type, "delete_reservation", "Can delete reservation"
    )
    view_reservation = get_permission(
        reservation_content_type, "view_reservation", "Can view reservation"
    )

    # Usuário
    usuario.permissions.add(
        view_resource,
        add_ticket,
        change_ticket,
        view_ticket,
        add_reservation,
        change_reservation,
        delete_reservation,
        view_reservation,
    )

    # Técnico
    tecnico.permissions.add(
        view_resource,
        add_resource,
        change_resource,
        add_ticket,
        change_ticket,
        view_ticket,
        view_reservation,
    )

    # Administrador
    admin.permissions.add(
        view_resource,
        add_resource,
        change_resource,
        delete_resource,
        add_ticket,
        change_ticket,
        view_ticket,
        delete_ticket,
        add_reservation,
        change_reservation,
        delete_reservation,
        view_reservation,
        add_customuser,
        change_customuser,
        delete_customuser,
        view_customuser,
    )


def remove_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    Group.objects.filter(
        name__in=["usuario", "tecnico", "admin"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("resources", "0002_alter_resource_options"),
        ("tickets", "0001_initial"),
        ("reservations", "0002_alter_reservation_usuario"),
    ]

    operations = [
        migrations.RunPython(
            create_groups_and_permissions,
            remove_groups_and_permissions,
        ),
    ]
