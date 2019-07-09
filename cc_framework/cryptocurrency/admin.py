from django.contrib import admin

from .models import Node, Currency, Address, Transaction

admin.site.register(Node)
admin.site.register(Currency)
admin.site.register(Address)
admin.site.register(Transaction)
