import graphene
from graphene_django.types import DjangoObjectType
from autores.models import Autor
from libros.models import Libro


class LibroType(DjangoObjectType):
    class Meta:
        model = Libro
        fields = ("id", "titulo", "isbn", "editorial", "anio_publicacion")


class AutorType(DjangoObjectType):
    libros = graphene.List(LibroType)

    class Meta:
        model = Autor
        fields = ("id", "nombre", "cedula", "nacionalidad", "fecha_nacimiento")

    def resolve_libros(self, info):
        return self.libros.all()


# Definir las Queries
class Query(graphene.ObjectType):
    all_autores = graphene.List(AutorType)
    autor_por_cedula = graphene.Field(AutorType, cedula=graphene.String(required=True))

    def resolve_all_autores(self, info):
        return Autor.objects.all()

    def resolve_autor_por_cedula(self, info, cedula):
        return Autor.objects.get(cedula=cedula)


# Definir las Mutations
class CreateAutor(graphene.Mutation):
    class Arguments:
        nombre = graphene.String()
        cedula = graphene.String()
        nacionalidad = graphene.String()
        fecha_nacimiento = graphene.Date()

    autor = graphene.Field(AutorType)

    def mutate(self, info, nombre, cedula, nacionalidad, fecha_nacimiento):
        if Autor.objects.filter(cedula=cedula).exists():
            raise Exception("Ya existe un autor con esa cédula")

        autor = Autor(
            nombre=nombre,
            cedula=cedula,
            nacionalidad=nacionalidad,
            fecha_nacimiento=fecha_nacimiento,
        )
        autor.save()
        return CreateAutor(autor=autor)


class UpdateAutor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        cedula = graphene.String()
        nombre = graphene.String()
        nacionalidad = graphene.String()
        fecha_nacimiento = graphene.Date()

    autor = graphene.Field(AutorType)

    def mutate(self, info, id, **kwargs):
        autor = Autor.objects.get(id=id)

        for key, value in kwargs.items():
            setattr(autor, key, value)

        autor.save()
        return UpdateAutor(autor=autor)


class DeleteAutor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        autor = Autor.objects.get(id=id)
        autor.delete()
        return DeleteAutor(ok=True)


class Mutation(graphene.ObjectType):
    create_autor = CreateAutor.Field()
    update_autor = UpdateAutor.Field()
    delete_autor = DeleteAutor.Field()


# Definir el schema principal
schema = graphene.Schema(query=Query, mutation=Mutation)
