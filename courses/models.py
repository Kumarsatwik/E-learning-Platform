from django.db import models
from django.contrib.auth.models import User
# Create your models here.
	
class Course(models.Model):
	name=models.CharField(max_length=50,null=False)
	slugs=models.CharField(max_length=50,null=False,unique=True)
	description=models.CharField(max_length=200,null=True)
	price=models.IntegerField(null=False,default=0)
	discount=models.IntegerField(null=False,default=0)
	active=models.BooleanField(default=False)
	thumbnail=models.ImageField(upload_to="image/thumbnail")
	date=models.DateTimeField(auto_now_add=True)
	length=models.IntegerField(null=False)
	resource=models.FileField(upload_to="image/resource")

	def __str__(self):
		return self.name

class CourseProperty(models.Model):
	description=models.CharField(max_length=200,null=False)
	course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)

	class Meta:
		abstract=True

class Tag(CourseProperty):
	pass

class Prerequisite(CourseProperty):
	pass

class Learning(CourseProperty):
	pass

class Video(models.Model):
	title=models.CharField(max_length=100,null=False)
	course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
	serial_number=models.IntegerField(null=False)
	video_id=models.CharField(max_length=200,null=False)
	is_preview=models.BooleanField(default=False)

	def __str__(self):
		return self.title

class UserCourse(models.Model):
	user=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username}->{self.course.name}'

class Payment(models.Model):
	order_id=models.CharField(max_length=60,null=False)
	payment_id=models.CharField(max_length=60)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	user_course=models.ForeignKey(UserCourse,null=True,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now_add=True)
	status=models.BooleanField(default=False)
	amount=models.FloatField(default=0)
	
 

class CouponCode(models.Model):
	code=models.CharField(max_length=6)
	course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='coupons')
	discount=models.IntegerField(default=0)

class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	course=models.CharField(max_length=256)
	date=models.DateTimeField(auto_now_add=True)
	slugs=models.CharField(max_length=256,null=False,unique=True)
	price=models.IntegerField(default=0)

	def __str__(self):
		return f'{self.user}->{self.course}'

class Review(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	subject=models.CharField(max_length=100,blank=True)
	review=models.TextField(max_length=500,blank=True)
	rating=models.FloatField()
	status=models.BooleanField(default=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)