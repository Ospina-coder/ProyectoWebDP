import graphene
from graphene_django.types import DjangoObjectType
from .models import Autor


# Definir el tipo de datos Autor
class AutorType(DjangoObjectType):
    class Meta:
        model = Autor
        fields = ("id", "nombre", "cedula", "nacionalidad", "fecha_nacimiento")


# Definir las Queries
class Query(graphene.ObjectType):
    all_autores = graphene.List(AutorType)

    def resolve_all_autores(self, info):
        return Autor.objects.all()


# Definir las Mutations
class CreateAutor(graphene.Mutation):
    class Arguments:
        nombre = graphene.String()
        cedula = graphene.String()
        nacionalidad = graphene.String()
        fecha_nacimiento = graphene.Date()

    autor = graphene.Field(AutorType)

    def mutate(self, info, nombre, cedula, nacionalidad, fecha_nacimiento):
        autor = Autor(
            nombre=nombre,
            cedula=cedula,
            nacionalidad=nacionalidad,
            fecha_nacimiento=fecha_nacimiento,
        )
        autor.save()
        return CreateAutor(autor=autor)


class Mutation(graphene.ObjectType):
    create_autor = CreateAutor.Field()


# Definir el schema principal
schema = graphene.Schema(query=Query, mutation=Mutation)
