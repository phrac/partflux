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
    part = Part.objects.get(id=part_id)
    exclude.append(part)
    xrefs.append(part)
    
    for p in part.cross_references.all():
        if p in xrefs or p in exclude:
            pass
        else:
            xrefs.append(p)
            subs = get_xrefs(p.id, exclude)
            for s in subs:
                if s in xrefs:
                    pass
                else:
                    xrefs.append(s)
    
    return xrefs

        
        
        
        
        
    





