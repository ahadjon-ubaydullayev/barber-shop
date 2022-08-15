from django.db import models
from django.contrib.auth.models import User


class BotUser(models.Model):
	user_id = models.IntegerField(unique=True)
	first_name = models.CharField(max_length=256, blank=True, null=True)
	tel_number = models.CharField(max_length=512, blank=True, null=True)
	active = models.BooleanField(default=False)
	permission = models.CharField(max_length=255, blank=True, null=True)
	language = models.CharField(max_length=255, blank=True, null=True)
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
	is_created = models.BooleanField(default=False)
	
	def str(self):
		return f'user id : {self.user_id}'


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
	bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.bot_user.first_name


# class WorkSchedule(models.Model):
# 	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
# 	start = models.CharField(max_length=12)
# 	end = models.CharField(max_length=12)
# 	status = models.BooleanField(default=False)
# 	date = models.DateField(auto_now_add=True)
# 	step = models.IntegerField(default=0)

# 	def __str__(self):
# 		return self.start


class EmployeeSchedule(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	start_time = models.CharField(max_length=128, null=True, blank=True)
	end_time = models.CharField(max_length=128, null=True, blank=True)
	status = models.BooleanField(default=False)
	step = models.IntegerField(default=0)
	
	def __str__(self):
		return self.start_time


class Order(models.Model):
	bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	order_time = models.CharField(max_length=12)
	status = models.BooleanField(default=False)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return f'{self.employee.user_id}'


class MessageStep(models.Model):
	step = models.IntegerField(default=0)

