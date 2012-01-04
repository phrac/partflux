def part_count(request):
	from parts.models import Part
	return{'part_count': Part.objects.count()}


