from django.core.exceptions import PermissionDenied


class OwnerOrPrivilegedRequiredMixin:
    privileged_group_names = ("tecnico", "admin")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        is_privileged = (
            user.is_superuser
            or user.groups.filter(
                name__in=self.privileged_group_names
            ).exists()
        )

        if obj.usuario_id != user.pk and not is_privileged:
            raise PermissionDenied

        return obj
