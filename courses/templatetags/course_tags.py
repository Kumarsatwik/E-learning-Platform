from django import template
import time
from courses.models import UserCourse
register=template.Library()

@register.simple_tag
def sellprice(price,discount):
	if discount==None or discount == 0:
		return price
	sellprice=price-(price*discount*0.01)
	return int(sellprice)
	
@register.filter(name='currency')
def currency(price):
	return "₹"+str(price)

@register.filter(name="greeting")
def greeting(name):
	name=str(name)
	current_time=time.localtime()
	if current_time.tm_hour<12 and current_time.tm_hour>5:
		return "Good Morning ,"+name
	elif current_time.tm_hour>11 and current_time.tm_hour<18:
		return "Good AfterNoon ,"+name
	elif current_time.tm_hour>18 and current_time.tm_hour<21:
		return "Good Evening ,"+name
	else:
		return "Good Night ,"+name

@register.filter(name="actual_amount")
def actual_amount(amount):
	print(amount)
	print(type(amount))
	return amount

@register.simple_tag
def isenrolled(request,course):
	isenrolled=False
	if not request.user.is_authenticated:
		return False
	user=request.user
	try:
		user_course=UserCourse.objects.get(user=user,course=course)
		return True
	except:
		return False

	return isenrolled

	