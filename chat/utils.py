from channels.db import database_sync_to_async


def get_something(model, **kwargs):
    """
    Gets a model object from a model by the slug
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


@database_sync_to_async
def aget_something(model, **kwargs):
    """
    Gets a model object from a model by the slug
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
