import factory

from CornershopTest.menus.models import Menu, Options


class OptionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Options

    name = factory.Sequence(lambda n: f"name_{n}")
    content = factory.Sequence(lambda n: f"content_{n}")


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    date = factory.Faker("date")

    @factory.post_generation
    def options(self, create, extracted):
        if not create:
            return
        if extracted:
            for option in extracted:
                self.options.add(option)
