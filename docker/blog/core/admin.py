from django.contrib import admin
from .models import Profile
from .models import Post, Category , Comment ,ForbiddenWords

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ForbiddenWords)



#
