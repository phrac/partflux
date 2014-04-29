from celery import task
from parts.models import Part

@task()
def update_all_xrefs(part_id):
    part = Part.objects.get(id=part_id)
    xrefs = get_xrefs(part_id)
    for x in xrefs:
        for p in xrefs:
            x.cross_references.add(p)

def get_xrefs(part_id, exclude=[]):
    xrefs = []
    sub = []
    part = Part.objects.get(id=part_id)
    for p in part.cross_references.all():
        xrefs.append(p)
        if p in exclude:
            pass
        else:
            
            sub = get_xrefs(p.id, exclude=xrefs)
    for s in sub:
        xrefs.append(s)

    return xrefs





