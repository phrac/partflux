def part_count(request):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = 'parts_part'")
    row = cursor.fetchone()
    return {
        'part_count': int(row[0])
    }

def nsn_count(request):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = 'nsn_nsn'")
    row = cursor.fetchone()
    return {
        'nsn_count': int(row[0])
    }

def xref_count(request):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = 'parts_xref'")
    row = cursor.fetchone()
    return {
        'xref_count': int(row[0])
    }

def company_count(request):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = 'companies_company'")
    row = cursor.fetchone()
    return {
        'company_count': int(row[0])
    }

def attr_count(request):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = 'parts_attribute'")
    row = cursor.fetchone()
    return {
        'attr_count': int(row[0])
    }

def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }

def get_current_domain(request):
    from django.contrib.sites.models import Site
    return {
        'current_domain': 'http://%s' % Site.objects.get_current().domain
    }

def user_reputation(request):
    from django.contrib.auth.models import User
    from users.models import UserProfile
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        return { 'user_reputation': profile.reputation }
    else:
        return { 'user_reputation': None }

