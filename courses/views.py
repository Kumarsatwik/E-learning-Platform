from django.shortcuts import render,redirect
from courses.models import *
from courses.forms import registrationForm,loginForm
from django.views import View
from django.http import HttpResponse,FileResponse
from django.contrib.auth import logout
from onlinecourses.settings import *
from time import time
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from math import ceil
from django.contrib.auth import get_user_model
# Create your views here.
import random
import io
from reportlab.pdfgen import canvas
import razorpay


client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
#myprofile
def myprofile(request):
	if request.method=="POST":
		username=request.POST['username']
		email=request.POST['emailaddress']
		user=User.objects.get(username=request.user)
		user.username=username
		user.email=email
		user.save()
		payment=Payment.objects.filter(user=request.user)
		details=get_user_model().objects.filter(username=request.user)
		wishlist=Wishlist.objects.filter(user=request.user)
		user_details={
			'name':request.user.username,
			'email':request.user.email
		}
		return render(request,'courses/myprofile.html',{'payments':payment,'detail':details,'wishlist':wishlist,'user':user_details})
	else:
		payment=Payment.objects.filter(user=request.user)
		details=get_user_model().objects.filter(username=request.user)
		wishlist=Wishlist.objects.filter(user=request.user)
		user_details={
			'name':request.user.username,
			'email':request.user.email
		}
		return render(request,'courses/myprofile.html',{'payments':payment,'detail':details,'wishlist':wishlist,'user':user_details})

#receipt pdf generate
def receipt(request,order):
	receipt_details=Payment.objects.get(order_id=order)
	print(receipt_details.date,receipt_details.user,receipt_details.payment_id,receipt_details.course)
	buf=io.BytesIO()
	c=canvas.Canvas(buf,pagesize=(400,400))
	textob=c.beginText()
	textob.setTextOrigin(10,300)
	textob.setFont("Helvetica",10)
	lines=[
		'Money Recipt From Udemy',
		f'Hello {receipt_details.user},'
		f'You Purchased {receipt_details.course} Course', 
		f'In {receipt_details.amount} Ruppess on {receipt_details.date}',
		f'Your Order Id is {receipt_details.order_id}',
		f'Your Payment Id is {receipt_details.payment_id}',
	]

	for text in lines:
		textob.textLine(text)
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)
	return FileResponse(buf,as_attachment=True,filename=f"{receipt_details.course}.pdf")

#reviews
def review_rate(request,product_id):
	if request.method=="POST":
		try:
			#review=Review.objects.get(course)
			pass
		except:
			pass
#wishlist 
def wishlist(request,slugs):
	course_details=Course.objects.get(slugs=slugs)
	messages=None
	#print(course_details)
	try:
		Wishlist_check=Wishlist.objects.get(slugs=slugs)
		print(Wishlist_check)
		messages="Already"
	except:
		add_wishlist=Wishlist(user=request.user,
					course=course_details.name,
					slugs=slugs,
					price=course_details.price
					)
		add_wishlist.save()
	course=Course.objects.all()
	random_number=random.randrange(1,len(course))
	random_topic=Course.objects.filter(id=random_number)
	return render(request,'courses/home.html',{'courses':course,'randoms':random_topic,'messages':messages})
	
def search_course(request):
	if request.method=='POST':
		search=request.POST['search']
		data=Course.objects.filter(name__icontains=search)
		discounted_course=Course.objects.all().order_by("discount")
		return render(request,'courses/search_course.html',{'searched':data,'discounted':discounted_course})
	else:
		return render(request,'courses/search_course.html')

def sample(request):
	course=Course.objects.all()
	random_number=random.randrange(1,len(course))
	random_topic=Course.objects.filter(id=random_number)
	n=len(course)
	nslides=n//4+ceil((n/4)-(n//4))
	if str(request.user)  =="AnonymousUser":
		return render(request,"courses/home.html",{'courses':course,'randoms':random_topic,'no_of_slides':n,'range':range(nslides)})
	return render(request,"courses/home.html",{'courses':course,'randoms':random_topic,'no_of_slides':n,'range':range(nslides)})
	
# course page

def coursePage(request,slugs):
	course=Course.objects.get(slugs=slugs)
	serial=request.GET.get('lecture')
	if serial is None:
		serial=1
	#print(serial)
	video=Video.objects.get(serial_number=serial,course=course)
	videos=course.video_set.all().order_by("serial_number")
	if video.is_preview is False:
		if request.user.is_authenticated is False: 
			return redirect('login')
		else:
			user=request.user
			try:
				user_course=UserCourse.objects.get(user=user,course=course)
			except:
				return redirect('checkout',slugs=course.slugs)
	return render(request,'courses/coursepage.html',{'course':course,'video':video,'videos':videos})
		

#signup

class signup(View):
	def get(self,request):
		print("get")
		form=registrationForm()
		return render(request,"courses/signup.html",{'form':form})
	def post(self,request):
		#print("post")
		form=registrationForm(request.POST)
		if(form.is_valid()):
			#print("Valid")
			user=form.save()
			if user is not None:
				#print("verified")
				return redirect('login')
		return render(request,"courses/signup.html",{"form":form}) 


#login

class login(View):
	def get(self,request):
		form=loginForm()
		return render(request,'courses/login.html',{'form':form})
	def post(self,request):
		form=loginForm(request=request,data=request.POST)
		if form.is_valid():
			return redirect('home')
		return render(request,'courses/login.html',{'form':form})

#logout

def signout(request):
	logout(request)
	return redirect("home")


#checkout

def checkout(request,slugs):
	course=Course.objects.get(slugs=slugs)
	user=None
	order=None
	payment=None
	couponmsg=""
	coupon=None
	if not request.user.is_authenticated: 
		return redirect('login')
	else:
		user=request.user
		action=request.GET.get('action')
		couponcode=request.GET.get('couponcode')		
		error=None
		amount=None
		try:
			user_course=UserCourse.objects.get(user=user,course=course)
			error="You already Purchased this Course"
		except:
			pass
		if error is None:
			amount=int((course.price-(course.price*course.discount*0.01))*100)
		if couponcode:
			try:
				coupon=CouponCode.objects.get(course=course,code=couponcode)
				amount=int((course.price*coupon.discount*0.01)*100)
				couponmsg="CouponCode Applied"
			except:
				couponmsg="Invalid Coupon"

		#print(amount)
		if amount == 0:
			user_course=UserCourse(user=user,course=course)
			user_course.save()
			course=Course.objects.all()
			return redirect("/")
		

		if action=='create_payment':
				
			currency="INR"
			receipt=f"onlinecourse-{int(time())}"
			notes={
					"email":user.email,
					"name":f'{user.first_name} {user.last_name}'
			}
 
			order = client.order.create({ "amount": amount, "currency": "INR", "receipt": receipt,"notes":notes })	
			#print(order)
			payment=Payment()
			payment.user=user
			payment.course=course
			payment.amount=amount/100
			payment.order_id=order.get('id')
			payment.save()
			try:
				Wishlist.objects.get(slugs=slugs).delete()
			except:
				print("Something goes wrong")
	
	
	context={
			'course':course,
			'error':error,
			'order':order,
			'payment':payment,
			'user':user,
			'couponmsg':couponmsg,
			'coupon':coupon
			}

	return render(request,'courses/checkout.html',context=context)
		


@csrf_exempt
def verify_payment(request):
	if request.method=="POST":
		data=request.POST
		context={}
		try:
			client.utility.verify_payment_signature(data)
			razorpay_order_id=data['razorpay_order_id']
			razorpay_payment_id=data['razorpay_payment_id']
			#print("Razor")
			payment=Payment.objects.get(order_id=razorpay_order_id)
			payment.payment_id=razorpay_payment_id
			payment.status=True	
			userCourse=UserCourse(user=payment.user,course=payment.course)
			userCourse.save()

			payment.user_course=userCourse
			payment.save()	
			context={
				'payment':payment
			}
			return render(request,"courses/test.html",context=context)
		except:
			
			return render(request,'courses/test.html')

		
	return redirect('home')

#my course
@login_required(login_url="login")
def my_course(request):
	user=request.user
	course=UserCourse.objects.filter(user=user)
	context={
		'user_course':course,
	}
	return render(request,"courses/my_course.html",context=context)