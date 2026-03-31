import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from usuarios.models import Perfil
from django.db import transaction


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class PerfilType(DjangoObjectType):
    class Meta:
        model = Perfil
        fields = ("id", "rol")


class Query(graphene.ObjectType):
    all_usuarios = graphene.List(UserType)

    def resolve_all_usuarios(self, info):
        return User.objects.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()
        rol = graphene.String()

    user = graphene.Field(UserType)
    perfil = graphene.Field(PerfilType)

    def mutate(self, info, username, email, password, rol):
        if User.objects.filter(username=username).exists():
            raise Exception("Ya existe un usuario con ese nombre de usuario")
        with transaction.atomic():
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            perfil = Perfil.objects.get(usuario=user)
            perfil.rol = rol
            perfil.save()

        return CreateUser(user=user, perfil=perfil)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
