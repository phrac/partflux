from celery import task

@task()
def update_all_xrefs(part_id):
    from parts.models import Part
    part = Part.objects.get(id=part_id)
    for p in part.cross_references.all():
        p.cross_references.add(part)
        update_all_xrefs(p.id)
