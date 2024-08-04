from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(DoddyUser)
admin.site.register(Auction)
admin.site.register(AuctionBet)
admin.site.register(FarmType)
admin.site.register(UserFarm)
