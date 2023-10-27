
# TODO: Try to use this method to trigger signal that changes unique_name
# TODO: User RegEx for _filename
def set_unique_name(instance) -> None:
    _filename = instance.image.name.split('/')[-1]
    instance.__class__.objects.filter(pk=instance.pk).update(
        unique_name=_filename)
