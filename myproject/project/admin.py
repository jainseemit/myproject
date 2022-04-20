from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(News)
admin.site.register(Guest)
admin.site.register(Visitors)
admin.site.register(Complain)
admin.site.register(Contact)