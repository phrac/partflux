def xrefs_handler(sender, instance, **kwargs):
    from parts.tasks import update_all_xrefs
    update_all_xrefs.delay(instance.id)
