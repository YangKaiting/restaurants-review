from django.contrib import admin
from .models import *
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(LikeForReview)
admin.site.register(Comment)
admin.site.register(LikeForComment)
