from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(unique=True, null=True)
	username = models.CharField(max_length=200, unique=True)
	bio = models.TextField(null=True)

	image = models.ImageField(null=True, upload_to='study_img/', default='img/pxxp.jpg')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username','name']

	def __str__(self):
		return self.username




class Topic(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name



class Room(models.Model):
	host = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)
	name = models.CharField(max_length=200)
	description = models.TextField(null=True, blank=True)
	participants = models.ManyToManyField(User, related_name='participants', blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-updated', '-created']

	def __str__(self):
		return self.name



class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	body = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-updated', '-created']

	
	def __str__(self):
		return self.body[:50]















