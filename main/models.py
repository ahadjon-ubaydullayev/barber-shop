from django.db import models
from django.contrib.auth.models import User

class BotUser(models.Model):
	user_id = models.IntegerField(unique=True)
	first_name = models.CharField(max_length=256, blank=True, null=True)
	tel_number = models.CharField(max_length=512, blank=True, null=True)
	active = models.BooleanField(default=False)
	permission = models.CharField(max_length=255, blank=True, null=True)
	cr_on = models.DateTimeField(auto_now_add=True)
	

	def __str__(self):
		return self.first_name


class Employee(models.Model):
	user_id = models.IntegerField(unique=True)
	step = models.IntegerField(default=0)
	full_name = models.CharField(max_length=256, blank=True, null=True)
	tel_number = models.CharField(max_length=512, blank=True, null=True)
	active = models.BooleanField(default=False)
	work_experience = models.CharField(max_length=256, blank=True, null=True)
	
	

	def __str__(self):
		return self.full_name


class ServiceCosts(models.Model):
	name = models.CharField(max_length=255)
	cost = models.CharField(max_length=255)

	def __str__(self):
		return self.name


class Styles(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


class Customer(models.Model):
	user_id = models.IntegerField(unique=True)
	first_name = models.CharField(max_length=256, blank=True, null=True)
	tel_number = models.CharField(max_length=512, blank=True, null=True)
	active = models.BooleanField(default=False)
	permission = models.CharField(max_length=255, blank=True, null=True)
	cr_on = models.DateTimeField(auto_now_add=True)
	

	def __str__(self):
		return self.first_name