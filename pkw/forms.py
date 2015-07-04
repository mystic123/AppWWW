# -*- coding: utf-8 -*-
from django import forms
from pkw import models

class InsertDataForm(forms.Form):
	recv_votes = forms.IntegerField(min_value = 0, label="Otrzymanych kart", initial=0)
	allowed_vote = forms.IntegerField(min_value = 0, label="Uprawnionych do głosowania", initial=0)
	updates = forms.IntegerField(widget=forms.HiddenInput())
	comm_id = forms.IntegerField(widget=forms.HiddenInput())

	def clean_updates(self):
		print("clean_updates")
		up = self.cleaned_data['updates']
		c_id = self.data['comm_id']
		comm_db = models.Commission.objects.filter(id = c_id)[0]
		print('updates: ', up)
		print('db_updates: ', comm_db.updates)
		if up != comm_db.updates:
			raise forms.ValidationError("Dane, które próbujesz zmienić zostały zmienione od ostatniego odczytu! Wprowadź je ponownie.")
		return up
