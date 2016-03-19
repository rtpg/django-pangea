from __future__ import unicode_literals

from django.db import models

# Create your models here.
from pangea import P


class Client(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    priority = models.IntegerField()
    name_format = models.CharField(choices=(('us', 'First Name First'),
                                            ('jp', 'Last Name First')), max_length=3)



    display_name = P.Case(
        (P.When(name_format='us'), P.Concat(P('first_name'), ' ', P('last_name'))),
        (P.When(name_format='jp'), P.Concat(P('last_name'), ' ', P('first_name'))),
        (P.Else, 'Undefined Name')
    )

    priority_display = P.Case(
        (P.When(priority__lte=3), 'Low'),
        (P.When(priority=4), 'Med'),
        (P.When(priority__gte=5), 'High')
    )


def get_client_names_from_queryset(clients):
    Client.objects.annotate(display_name=Client.display_name).values_list('display_name')


def get_client_names_from_list(clients):
    return [c.display_name() for c in clients]
