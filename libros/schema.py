import graphene
from graphene_django.types import DjangoObjectType
from libros.models import Libro
from autores.models import Autor
from libros.services import obtener_datos_libro_por_isbn


class AutorType(DjangoObjectType):
    class Meta:
        model = Autor
        fields = ("id", "cedula", "nombre", "nacionalidad", "fecha_nacimiento")


class LibroType(DjangoObjectType):
    class Meta:
        model = Libro
        fields = (
            "id",
            "titulo",
            "isbn",
            "editorial",
            "anio_publicacion",
            "autor",
            "portada_url",
            "titulo_api",
            "editorial_api",
        )


class Query(graphene.ObjectType):
    all_libros = graphene.List(LibroType)

    def resolve_all_libros(self, info):
        return Libro.objects.all()


class CreateLibro(graphene.Mutation):
    class Arguments:
        titulo = graphene.String(required=True)
        isbn = graphene.String(required=True)
        editorial = graphene.String(required=True)
        anio_publicacion = graphene.Int(required=True)
        autor_id = graphene.Int(required=True)

    libro = graphene.Field(LibroType)

    def mutate(self, info, titulo, isbn, editorial, anio_publicacion, autor_id):
        try:
            autor = Autor.objects.get(id=autor_id)
        except Autor.DoesNotExist:
            raise Exception("No existe un autor con ese ID")

        if Libro.objects.filter(isbn=isbn).exists():
            raise Exception("Ya existe un libro con ese ISBN")

        datos_api = obtener_datos_libro_por_isbn(isbn)

        libro = Libro(
            titulo=titulo,
            isbn=isbn,
            editorial=editorial,
            anio_publicacion=anio_publicacion,
            autor=autor,
            portada_url=datos_api.get("portada_url"),
            titulo_api=datos_api.get("titulo_api"),
            editorial_api=datos_api.get("editorial_api"),
        )
        libro.save()
        return CreateLibro(libro=libro)


class UpdateLibro(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        titulo = graphene.String()
        isbn = graphene.String()
        editorial = graphene.String()
        anio_publicacion = graphene.Int()
        autor_id = graphene.Int()

    libro = graphene.Field(LibroType)

    def mutate(self, info, id, **kwargs):
        libro = Libro.objects.get(id=id)

        if "autor_id" in kwargs:
            try:
                autor = Autor.objects.get(id=kwargs["autor_id"])
                libro.autor = autor
            except Autor.DoesNotExist:
                raise Exception("No existe un autor con ese ID")
            kwargs.pop("autor_id")

        for key, value in kwargs.items():
            setattr(libro, key, value)

            datos_api = obtener_datos_libro_por_isbn(libro.isbn)
            if datos_api:
                libro.portada_url = datos_api.get("portada_url")
                libro.titulo_api = datos_api.get("titulo_api")
                libro.editorial_api = datos_api.get("editorial_api")

        libro.save()
        return UpdateLibro(libro=libro)


class DeleteLibro(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        libro = Libro.objects.get(id=id)
        libro.delete()
        return DeleteLibro(ok=True)


class Mutation(graphene.ObjectType):
    create_libro = CreateLibro.Field()
    update_libro = UpdateLibro.Field()
    delete_libro = DeleteLibro.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
