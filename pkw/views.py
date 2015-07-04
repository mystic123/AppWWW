from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from models import *
from django.http import JsonResponse
from forms import *
from django.db import transaction, DatabaseError
from django.shortcuts import redirect

# Create your views here.
def home(request):
	return render(request, 'index.html')
	
def getVoivs(request):
	voivs = Voivodeship.objects.all().order_by('name')
	return JsonResponse([v.json() for v in voivs], safe=False)

def getDistricts(request, voiv = None):
	districts = City.objects.filter(voiv__name = voiv)
	return JsonResponse([d.json() for d in districts], safe=False) 

def getCommCounty(request, voiv = None, dist = None):
	if ("." in dist or "Zagranica" in dist or "Statki" in dist):
		result = Commission.objects.filter(dist__name = dist).order_by('nr','name')
	else:
		result = County.objects.filter(city__name = dist)
	return JsonResponse([r.json() for r in result], safe=False)

def getComm(request, voiv = None, dist = None, county = None):
	comms = Commission.objects.filter(dist__name = county).order_by('nr','name')
	return JsonResponse([c.json() for c in comms], safe=False)

def getVotesData(request, id = None):
	comm = Commission.objects.get(id = id)
	result = {'recv_votes': comm.recv_votes, 'allowed_vote' : comm.allowed_vote, 'updates' : comm.updates}
	return JsonResponse(result, safe=False)

@transaction.atomic
def saveVotes(request, id = None):
	if request.method == "POST" and request.is_ajax():
		updates = request.POST.get("updates")
		recv_votes = request.POST.get("recv_votes")
		allowed_vote = request.POST.get("allowed_vote")
		try:
			comm = Commission.objects.select_for_update(nowait=True).get(id = id) 
		except DatabaseError as e:
			return JsonResponse({"locked" : True})
		if comm.updates == int(updates):
			with transaction.atomic():
				comm.updates += 1
				comm.recv_votes = recv_votes
				comm.allowed_vote = allowed_vote
				comm.save()
			response = {}
			response["updates"] = comm.updates
			response["success"] = True
			return JsonResponse(response)
	return JsonResponse({"success" : False})
