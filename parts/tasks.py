from celery import task
from parts.models import Part

@task()
def update_all_xrefs(part_id):
    part = Part.objects.get(id=part_id)
    xrefs = get_xrefs(part_id)
    for x in xrefs:
        for p in xrefs:
            x.cross_references.add(p)


def get_xrefs(part_id):
    xrefs = []
    part = Part.objects.get(id=part_id)
    xrefs.append(part)
    
    for p in part.cross_references.all():
        if p in xrefs:
            pass
        else:
            xrefs.append(p)
    
    for p in xrefs:
        xr = p.cross_references.all()
        for x in xr:
            if x in xrefs:
                pass
            else:
                xrefs.append(p)

    return xrefs





