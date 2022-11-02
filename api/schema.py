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
        username=graphene.String(required=True),
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
        task_id = graphene.ID(required=True)
        username = graphene.String(required=True)
        name = graphene.String(required=True)
        creation_date = graphene.DateTime(required=True)
        content = graphene.String()

    def mutate_and_get_payload(self, info, **kwargs):
        task = Todo.objects.create(**kwargs)
        task.save()

        return CreateTask(task)


class CloseTask(graphene.relay.ClientIDMutation):
    task = graphene.Field(Task)

    class Input:
        task_id = graphene.ID(required=True)
        username = graphene.String(required=True)
        closing_date = graphene.DateTime(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            task = Todo.objects.get(
                username=kwargs['username'],
                task_id=kwargs['task_id']
            )
        except Todo.DoesNotExist:
            raise Exception('Task not found on database!')

        if task.is_closed:
            raise Exception('Task is already closed!')

        task.closing_date = kwargs['closing_date']
        task.is_closed = True
        task.save()

        return CloseTask(task)


class ReopenTask(graphene.relay.ClientIDMutation):
    task = graphene.Field(Task)

    class Input:
        username = graphene.String(required=True)
        task_id = graphene.ID(required=True)
        reopen_date = graphene.DateTime(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            task = Todo.objects.get(
                username=kwargs['username'],
                task_id=kwargs['task_id']
            )
        except Todo.DoesNotExist:
            raise Exception('Task not found on database!')

        if not task.is_closed:
            raise Exception('Cannot reopen an open task!')

        task.is_closed = False
        task.reopen_date = kwargs['reopen_date']
        task.save()

        return ReopenTask(task)


class UpdateTask(graphene.relay.ClientIDMutation):
    task = graphene.Field(Task)

    class Input:
        username = graphene.String(required=True)
        task_id = graphene.ID(required=True)
        name = graphene.String()
        content = graphene.String()

    def mutate_and_get_payload(self, info, **kwargs):
        name = kwargs.get('name')
        content = kwargs.get('content')

        try:
            task = Todo.objects.get(
                username=kwargs['username'],
                task_id=kwargs['task_id']
            )
        except Todo.DoesNotExist:
            raise Exception('Task not found on database!')

        if task.is_closed:
            raise Exception('Cannot update an closed task!')

        if name:
            task.name = name
        if content:
            task.content = content

        task.save()

        return UpdateTask(task)


class Mutation:
    create_task = CreateTask.Field()
    close_task = CloseTask.Field()
    reopen_task = ReopenTask.Field()
    update_task = UpdateTask.Field()
