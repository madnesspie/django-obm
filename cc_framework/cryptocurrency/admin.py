from django.contrib import admin

from cryptocurrency import models

admin.site.register(models.Node)
admin.site.register(models.Currency)
admin.site.register(models.Address)
admin.site.register(models.Transaction)
