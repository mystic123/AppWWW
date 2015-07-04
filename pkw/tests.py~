import unittest
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.test import TestCase, Client
from django.db import transaction, IntegrityError
from pkw.models import *

# Create your tests here.

class PKWTestCase(TestCase):
	def setUp(self):
		v = Voivodeship.objects.create(name = "TestVoivodeship")
		c = City.objects.create(name = "some city", voiv = v)
		cnty = County.objects.create(name = "some county", city = c)
		comm1 = Commission.objects.create(nr = 1, name = "some commission", dist = c)
		comm2 = Commission.objects.create(nr = 2, name = "some other commission", dist = cnty)
		comm3 = Commission()
		comm3.nr = 5
		comm3.name = "comm3"
		comm3.dist = cnty
		comm3.recv_votes = 108
		comm3.allowed_vote = 123
		comm3.updates = 12
		comm3.save()

	def test_basics(self):
		v = Voivodeship.objects.get(name = "TestVoivodeship")
		city = City.objects.get(name = "some city")
		cnty = County.objects.get(name = "some county")
		c1 = Commission.objects.get(name = "some commission")
		c2 = Commission.objects.get(name = "some other commission")
		self.assertEqual(v.name, "TestVoivodeship")
		self.assertEqual(city.name, "some city")
		self.assertEqual(cnty.name, "some county")
		self.assertEqual(c1.name, "some commission")
		self.assertEqual(c1.nr, 1)
		self.assertEqual(c1.dist.name, city.name)
		self.assertEqual(c2.dist.name, cnty.name)

	def test_json(self):
		v = Voivodeship.objects.get(name = "TestVoivodeship")
		self.assertEqual(v.json()["name"], "TestVoivodeship")
		comm1 = Commission.objects.get(name = "comm3")
		dict1 = comm1.json()
		cnty = County.objects.get(name = "some county")
		self.assertEqual(dict1["dist"]["name"],"some county")
		self.assertEqual(dict1["comm"]["nr"], 5)
		self.assertEqual(dict1["comm"]["name"], "comm3")
		self.assertEqual(dict1["comm"]["recv_votes"], 108)
		self.assertEqual(dict1["comm"]["allowed_vote"], 123)
		self.assertEqual(dict1["comm"]["updates"], 12)

	def test_integrity(self):
		#integrity tests
		c1 = Commission.objects.get(name = "some commission")
		c2 = Commission.objects.get(name = "some other commission")
		with transaction.atomic():
			with self.assertRaises(IntegrityError):
				Voivodeship.objects.create(name = "TestVoivodeship")

		with transaction.atomic():
			with self.assertRaises(IntegrityError):
				City.objects.create(name = "some city")

		with transaction.atomic():
			with self.assertRaises(IntegrityError):
				County.objects.create(name = "some county")

		with transaction.atomic():
			with self.assertRaises(IntegrityError):
				City.objects.create(name = "some county")

		with transaction.atomic():
			c1.recv_votes = -5.2
			c1.allowed_vote = -23
			with self.assertRaises(IntegrityError):
				c1.save()

		with transaction.atomic():
			c2.allowed_vote = 10.2
			c2.save()
			c2 = Commission.objects.get(name = "some other commission")
			self.assertEqual(c2.allowed_vote, round(10.2))

class ClientTest(unittest.TestCase):
	def setUp(self):
		v = Voivodeship.objects.create(name = "TestVoivodeship")
		Voivodeship.objects.create(name = "TestVoivodeship 2")
		c = City.objects.create(name = "some city M.", voiv = v)
		c2 = City.objects.create(name = "some other city", voiv = v)
		cnty = County.objects.create(name = "some county", city = c2)
		County.objects.create(name = "some other county", city = c2)
		comm1 = Commission.objects.create(nr = 1, name = "some commission", dist = c)
		comm2 = Commission.objects.create(nr = 2, name = "some other commission", dist = cnty)
		Commission.objects.create(nr = 2, name = "some other city commission", dist = c)
		Commission.objects.create(nr = 3, name = "some other county commission", dist = cnty) 
		comm3 = Commission()
		comm3.nr = 5
		comm3.name = "comm3"
		comm3.dist = cnty
		comm3.recv_votes = 108
		comm3.allowed_vote = 123
		comm3.updates = 12
		comm3.save()
		self.client = Client()

	def test_details(self):
#testing json responses
		response = self.client.get("/")
		self.assertEqual(len(response.templates), 1)
		self.assertEqual(response.templates[0].name, "index.html")
		response = self.client.get("/req/")
		voivList = Voivodeship.objects.all()
		sort1 = sorted([repr(x) for x in response])
		sort2 = sorted([repr(x) for x in JsonResponse([v.json() for v in voivList], safe=False)])
		self.assertEqual(sort1, sort2)
		response = self.client.get("/req/"+voivList[0].name+"/")
		cityList = City.objects.all().filter(voiv = voivList[0])
		sort1 = sorted([repr(x) for x in response])
		sort2 = sorted([repr(x) for x in JsonResponse([c.json() for c in cityList], safe=False)])
		self.assertEqual(sort1, sort2)
		response = self.client.get("/req/"+voivList[0].name + "/" + cityList[0].name+"/")
		countyList = County.objects.all().filter(city = cityList[0])
		sort1 = sorted([repr(x) for x in response])
		sort2 = sorted([repr(x) for x in JsonResponse([c.json() for c in countyList], safe=False)])
		self.assertEqual(sort1, sort2)
		response = self.client.get("/req/"+voivList[0].name + "/" + cityList[0].name+"/" + countyList[1].name + "/")
		commList = Commission.objects.all().filter(dist = countyList[1])
		set1 = set([repr(x) for x in response])
		set2 = set([repr(x) for x in JsonResponse([c.json() for c in commList], safe=False)])
		self.assertEqual(sort1, sort2)
		comm = Commission.objects.get(nr = 5, name = "comm3")
		response = self.client.get("/req/votes/" + str(comm.id) + "/")
		resDict = json.loads(response.content)
		self.assertEqual(comm.recv_votes, resDict["recv_votes"])
		self.assertEqual(comm.allowed_vote, resDict["allowed_vote"])
		self.assertEqual(comm.updates, resDict["updates"])
#testing saving new correct data
		postDict = {"updates" : comm.updates, "recv_votes" : 900, "allowed_vote" : 1000}
		self.client.post("/req/votes/" + str(comm.id) + "/", )
		response = self.client.post("/req/save/" + str(comm.id) + "/", data=postDict, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		resDict = json.loads(response.content)
		self.assertEqual(resDict["updates"], comm.updates+1)
		self.assertEqual(resDict["success"], True)
		response = self.client.get("/req/votes/" + str(comm.id) + "/")
		resDict = json.loads(response.content)
		self.assertEqual(resDict["recv_votes"], 900)
		self.assertEqual(resDict["allowed_vote"], 1000)
		self.assertEqual(resDict["updates"], comm.updates+1)
#testing saving incorrect data
		postDict["updates"] = 123;
		response = self.client.post("/req/save/" + str(comm.id) + "/", data=postDict, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		resDict = json.loads(response.content)
		self.assertEqual(resDict["success"], False)


