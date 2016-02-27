from django.test import TestCase

# Create your tests here.
from client.models import Client, get_client_names_from_queryset


class ClientAccessTestCase(TestCase):
    def test_client_access(self):
        names = [('Shenika', 'Sola', 'us', 'Shenika Sola'),
                 ('Judith', 'Jetter', 'ja', 'Judith Jetter'),
                 ('Martin', 'Milholland', 'xh', 'Undefined Name')]

        for fst, snd, name_format, _ in names:
            Client.objects.create(
                first_name=fst,
                last_name=snd,
                name_format=name_format
            )

        formatted_names = set(n[3] for n in names)

        clients_qs = Client.objects.all()

        names_from_qs = clients_qs.annotate(result_name=Client.display_name).values('result_name')

        set_of_qs_names = set([n['result_name'] for n in names_from_qs])

        self.assertEqual(formatted_names, set_of_qs_names)

        # filter by the mechanism

        martin = Client.objects.annotate(display_name=Client.display_name)\
            .filter(display_name='Undefined Name').get()

        # Make sure it's martin
        self.assertEqual(martin.first_name, 'Martin')

        # check that we can simply call on the object themselves

        client_list = list(Client.objects.all())

        set_of_names_from_list = set(
            c.display_name() for c in client_list
        )

        self.assertEqual(set_of_names_from_list, formatted_names)
