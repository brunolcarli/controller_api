import graphene
from api.models import Todo


class Task(graphene.ObjectType):
    creation_date = graphene.DateTime()
    closing_date = graphene.DateTime()
    is_closed = graphene.Boolean()
    name = graphene.String()
    content = graphene.String()



class Query:
    version = graphene.String()

    def resolve_version(self, info, **kwargs):
        return '0.0.0'


    tasks = graphene.List(
        Task,
        name__icontains=graphene.String(),
        creation_date__gte=graphene.DateTime(),
        creation_date__lte=graphene.DateTime(),
        closing_date__gte=graphene.DateTime(),
        closing_date__lte=graphene.DateTime(),
        is_closed=graphene.Boolean()
    )

    def resolve_tasks(self, info, **kwargs):
        return Todo.objects.filter(**kwargs)


## Mutations

class CreateTask(graphene.relay.ClientIDMutation):
    task = graphene.Field(Task)

    class Input:
        name = graphene.String(required=True)
        creation_date = graphene.DateTime(required=True)
        content = graphene.String()

    def mutate_and_get_payload(self, info, **kwargs):
        task = Todo.objects.create(**kwargs)

        return CreateTask(task)


class Mutation:
    create_task = CreateTask.Field()
