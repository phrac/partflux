from django.shortcuts import render_to_response
from parts.models import Part

def index(request):
	parts_list = Part.objects.all().order_by('-created_at')[:5]
	return render_to_response('parts/index.html', {'parts_list': parts_list})



def detail(request):
	return HttpResponse("Hello, world. At index")


