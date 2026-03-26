import graphene
import autores.schema
import libros.schema
import usuarios.schema


class Query(
    autores.schema.Query,
    libros.schema.Query,
    usuarios.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    autores.schema.Mutation,
    libros.schema.Mutation,
    usuarios.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
