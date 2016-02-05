from apps.core.models import Area


def statics(request):
    areas = Area.objects.all()
    return {'areas': areas}