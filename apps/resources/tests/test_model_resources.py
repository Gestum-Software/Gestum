from django.test import TestCase

from apps.resources.models import Resource


class ResourcesModelTest(TestCase):

    def test_create_resource_with_required_fields(self):
        resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )

        self.assertEqual(Resource.objects.count(), 1)
        self.assertEqual(resource.nome, "Projetor")
        self.assertEqual(
            resource.observacoes,
            "Projetor disponível para empréstimo.",
        )

    def test_status_defaults_to_available(self):
        resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )

        self.assertEqual(resource.status, Resource.StatusChoices.DISPONIVEL)

    def test_status_can_be_set_to_maintenance(self):
        resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Necessita de reparo.",
            status=Resource.StatusChoices.EM_MANUTENCAO,
        )

        self.assertEqual(
            resource.status,
            Resource.StatusChoices.EM_MANUTENCAO,
        )

    def test_status_choices_are_defined(self):
        self.assertEqual(
            Resource.StatusChoices.choices,
            [
                ("disponivel", "Disponível"),
                ("manutencao", "Em Manutenção"),
            ],
        )

    def test_string_representation(self):
        resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
            status=Resource.StatusChoices.EM_MANUTENCAO,
        )

        self.assertEqual(str(resource), "Projetor | (manutencao)")

    def test_model_field_configuration(self):
        nome = Resource._meta.get_field("nome")
        observacoes = Resource._meta.get_field("observacoes")
        status = Resource._meta.get_field("status")

        self.assertEqual(nome.max_length, 50)
        self.assertEqual(observacoes.max_length, 1500)
        self.assertFalse(observacoes.blank)
        self.assertFalse(observacoes.null)
        self.assertEqual(status.max_length, 20)
        self.assertEqual(status.default, Resource.StatusChoices.DISPONIVEL)