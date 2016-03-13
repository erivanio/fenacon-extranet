from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__


@register.filter
def len_files(folder):
    folders = folder.children.filter(status=True).count()
    files = folder.file_set.filter(status=True).count()
    result = folders + files
    return result


@register.assignment_tag()
def has_area(user, area):
    if area in user.areas.all():
        return True
    for group in user.groups.all():
        if area in group.areas.all():
            return True
    return False


@register.filter
def has_share_permission(user):
    if 'compartilhar_arquivo_pasta' in user.permissions.values_list('slug', flat=True):
        return True
    for group in user.groups.all():
        if 'compartilhar_arquivo_pasta' in group.permissions.values_list('slug', flat=True):
            return True
    return False


@register.filter
def has_file_permission(user):
    if 'subir_arquivo' in user.permissions.values_list('slug', flat=True):
        return True
    for group in user.groups.all():
        if 'subir_arquivo' in group.permissions.values_list('slug', flat=True):
            return True
    return False


@register.filter
def has_folder_permission(user):
    if 'criar_pasta' in user.permissions.values_list('slug', flat=True):
        return True
    for group in user.groups.all():
        if 'criar_pasta' in group.permissions.values_list('slug', flat=True):
            return True
    return False


@register.filter
def has_remove_permission(user):
    if 'excluir_arquivo_pasta' in user.permissions.values_list('slug', flat=True):
        return True
    for group in user.groups.all():
        if 'excluir_arquivo_pasta' in group.permissions.values_list('slug', flat=True):
            return True
    return False


@register.filter
def has_history_permission(user):
    if 'vizualizar_historico' in user.permissions.values_list('slug', flat=True):
        return True
    for group in user.groups.all():
        if 'vizualizar_historico' in group.permissions.values_list('slug', flat=True):
            return True
    return False