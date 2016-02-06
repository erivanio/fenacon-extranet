from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__


@register.filter
def len_files(folder):
    folders = folder.children.all().count()
    files = folder.file_set.all().count()
    result = folders + files
    return result
