from django.db import models

# Create your models here.

class Voivodeship(models.Model):
	name = models.CharField(max_length=25, primary_key=True)

	def __unicode__(self):
		return self.name

	def json(self):
		return {
				'name' : self.name,
				}

class District(models.Model):
	name = models.CharField(max_length=100, primary_key=True)
	
	def __unicode__(self):
		return self.name

	def json(self):
		return {
				'name' : self.name,
				}

class City(District):
	voiv = models.ForeignKey(Voivodeship)

	def __unicode__(self):
		return self.name

	def json(self):
		return {'dist' : super(City,self).json(), 'voiv' : self.voiv.json()}
				
class County(District):
	city = models.ForeignKey(City)

	def __unicode__(self):
		return self.name

	def json(self):
		return {'dist' : super(County,self).json(),
				'city' : self.city.json()}

class Commission(models.Model):
	nr = models.PositiveIntegerField()
	name = models.CharField(max_length=200, null=False)
	dist = models.ForeignKey(District)
	recv_votes = models.PositiveIntegerField(default=0)
	allowed_vote = models.PositiveIntegerField(default=0)
	updates = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return unicode(self.nr) + ". " + self.name

	def json(self):
		this = {
				'nr' : self.nr,
				'name' : self.name,
				'recv_votes' : self.recv_votes,
				'allowed_vote' : self.allowed_vote,
				'id' : self.id,
				'updates' : self.updates
				}
		return {'comm' : this, 'dist' : self.dist.json()}
