from django.test import TestCase

# Create your tests here.
from client.models import Client


class ClientAccessTestCase(TestCase):

    def test_from_readme(self):

        client = Client.objects.create(
            first_name="Judith",
            last_name="Jetter",
            priority=10,
            name_format='jp',
        )

        # operate on a python object directly
        formatted_name = Client.display_name(client)

        self.assertEqual(formatted_name, "Jetter Judith")

        # get it in ORM operations by annotating it onto a queryset
        # the value can also be used for things like filtering
        formatted_name = Client.objects.annotate(
            display_name=Client.display_name.django()
        ).values_list('display_name')

        self.assertEqual(formatted_name[0], ("Jetter Judith",))

    def test_client_access(self):
        names = [('Shenika', 'Sola', 'us', 2, 'Shenika Sola'),
                 ('Judith', 'Jetter', 'jp', 4, 'Jetter Judith'),  # last name first
                 ('Martin', 'Milholland', 'xh', 7, 'Undefined Name')]

        for fst, snd, name_format, priority, _ in names:
            Client.objects.create(
                first_name=fst,
                last_name=snd,
                priority=priority,
                name_format=name_format
            )

        formatted_names = set(n[4] for n in names)

        # check that we can simply call on the object themselves

        client_list = list(Client.objects.all())

        set_of_names_from_list = set(
            Client.display_name(c) for c in client_list
        )

        self.assertEqual(set_of_names_from_list, formatted_names)

        clients_qs = Client.objects.all()

        names_from_qs = clients_qs.annotate(result_name=Client.display_name.django()).values('result_name')

        set_of_qs_names = set([n['result_name'] for n in names_from_qs])

        self.assertEqual(formatted_names, set_of_qs_names)

        # filter by the mechanism

        martin = Client.objects.annotate(display_name=Client.display_name.django())\
            .filter(display_name='Undefined Name').get()

        # Make sure it's martin
        self.assertEqual(martin.first_name, 'Martin')

        for c in client_list:
            p_d = Client.priority_display(c)
            if c.priority <= 3:
                self.assertEqual(p_d, 'Low')
            if c.priority == 4:
                self.assertEqual(p_d, 'Med')
            if c.priority >= 5:
                self.assertEqual(p_d, 'High')

        # check that priority is also working as a django expression real quick
        priorities = Client.objects.annotate(p=Client.priority_display.django())\
            .values_list('priority', 'p')

        for priority, display in priorities:
            if priority <= 3:
                self.assertEqual(display, 'Low')
            if priority == 4:
                self.assertEqual(display, 'Med')
            if priority >= 5:
                self.assertEqual(display, 'High')
