from django.contrib import admin
from courses.models import *
from django.utils.html import format_html
# Register your models here.

class tagAdmin(admin.TabularInline):
	model=Tag

class prerequisiteAdmin(admin.TabularInline):
	model=Prerequisite

class learningAdmin(admin.TabularInline):
	model=Learning

class videoAdmin(admin.ModelAdmin):
	class Meta:
		Fields='__all__'

class videoTAdmin(admin.TabularInline):
	model=Video

class courseAdmin(admin.ModelAdmin):
	inlines=[tagAdmin,learningAdmin,prerequisiteAdmin,videoTAdmin]
	list_display=["name","get_price","get_discount","active"]
	list_filter=("discount","active")
	def get_discount(self,course):
		return f'{course.discount} %'

	def get_price(self,course):
		return f'₹{course.price}'

	get_discount.short_description="Discount"
	get_price.short_description="Price"

class usercourseAdmin(admin.ModelAdmin):
	class Meta:
		Fields='__all__'

class paymentAdmin(admin.ModelAdmin):
	class Meta:
		Fields='__all__'

	list_display=["get_user","course","amount","status"]
	list_filter=["status","course"]

	def get_user(self,payment):
		return format_html(f"<a href='/adminauth/user/{payment.user.id}/'>{payment.user}</a>")

admin.site.register(UserCourse,usercourseAdmin)
admin.site.register(Payment,paymentAdmin)
admin.site.register(Course,courseAdmin)
admin.site.register(Video,videoAdmin)
admin.site.register(CouponCode)
admin.site.register(Wishlist)


