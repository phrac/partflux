from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello, world. At index")

def detail(request):
	return HttpResponse("Hello, world. At index")


