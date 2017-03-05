from __future__ import unicode_literals

from django.db import models
import datetime

class ScrapeData(models.Model):

	permit_number = models.CharField(max_length=255)
	status = models.CharField(max_length=255)
	address = models.CharField(max_length=555)
	contractor = models.CharField(max_length=1255)
	description = models.CharField(max_length=1555)
	valuation = models.CharField(max_length=255)
	licensed_professional = models.CharField(max_length=1255)
	parcel_number = models.CharField(max_length=5255)
	date_created = models.DateTimeField(default=datetime.datetime.now)

	def __unicode__(self):
		return self.address
