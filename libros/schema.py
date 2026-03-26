import graphene
from graphene_django.types import DjangoObjectType
from libros.models import Libro
from autores.models import Autor


# Define el tipo de datos Libro
class LibroType(DjangoObjectType):
    class Meta:
        model = Libro
        fields = ("id", "titulo", "isbn", "editorial", "anio_publicacion", "autor")


class Query(graphene.ObjectType):
    all_libros = graphene.List(LibroType)

    def resolve_all_libros(self, info):
        return Libro.objects.all()


class CreateLibro(graphene.Mutation):
    class Arguments:
        titulo = graphene.String()
        isbn = graphene.String()
        editorial = graphene.String()
        anio_publicacion = graphene.Int()
        autor_id = graphene.Int()

    libro = graphene.Field(LibroType)

    def mutate(self, info, titulo, isbn, editorial, anio_publicacion, autor_id):
        autor = Autor.objects.get(id=autor_id)
        libro = Libro(
            titulo=titulo,
            isbn=isbn,
            editorial=editorial,
            anio_publicacion=anio_publicacion,
            autor=autor,
        )
        libro.save()
        return CreateLibro(libro=libro)


class Mutation(graphene.ObjectType):
    create_libro = CreateLibro.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
