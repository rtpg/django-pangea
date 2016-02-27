from __future__ import unicode_literals

from django.db import models

# Create your models here.
from pangea import P


class Client(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    name_format = models.CharField(choices=(('us', 'First Name First'),
                                            ('jp', 'Last Name First')), max_length=3)



    display_name = P.Case(
        (P('name_format') == 'us', P.Concat(P('first_name'), ' ', P('last_name'))),
        (P('name_format') == 'jp', P.Concat(P('last_name'), ' ', P('first_name'))),
        (P.Else, 'Undefined Name')
    )


def get_client_names_from_queryset(clients):
    Client.objects.annotate(display_name=Client.display_name).values_list('display_name')


def get_client_names_from_list(clients):
    return [c.display_name() for c in clients]
