Pangea : Use your model methods anywhere
========

  This package provides a small DSL to let you write simple model methods that
will work both when operating the ORM and when working with native python objects.

  This helps to maintain a seperation between the "What" and the "Why " in your
business logic, without having to maintain seperate code blocks for different
querying situations.

```
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
        (P.When(priority__gte=5), 'High'),
        django_output_field=models.CharField(),
    )
```

After you have defined a Pangea expression, you can either cast it into the ORM space
(through `django`) or into the native python object space (by calling the expression directly)

```
        client = Client.objects.create(
            first_name="Judith",
            last_name="Jetter",
            priority=10,
            name_format='jp',
        )

        # operate on a python object directly
        formatted_name = Client.display_name(client)
        # formatted_name == "Jetter Judith"

        # get it in ORM operations by annotating it onto a queryset
        # the value can also be used for things like filtering
        formatted_name = Client.objects.annotate(
            display_name=Client.display_name.django()
        ).values_list('display_name')

        # formatted_name[0] == ("Jetter Judith",)
```

 Currently Pangea only supports this basic use case (with possible extensions to more single-table expressions). Still researching how to enable this on more complicated multi-table expressions with joins and the like.

 This is still in a very experimental state, but feel free to file issues for any feature requests that you might want!
