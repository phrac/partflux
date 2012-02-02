def part_count(request):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = 'parts_part'")
    row = cursor.fetchone()
    return {
        'part_count': int(row[0])
    }

def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }


