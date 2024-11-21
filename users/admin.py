from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, Employee, EmployeeAvailability

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(EmployeeAvailability)