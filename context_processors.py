def part_count(request):
	from parts.models import Part
	return {
        'part_count': Part.objects.count()
    }

def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }


