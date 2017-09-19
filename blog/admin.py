from django.contrib import admin
from blog.models import Article,ArticleDetail,Article2Tag,ArticleUpDown,\
    Comment,Category,CommentUp,UserInfo,Tag,UserFans,Blog

# Register your models here.


admin.site.register(ArticleDetail)
admin.site.register(Article)
admin.site.register(Article2Tag)
admin.site.register(ArticleUpDown)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(CommentUp)
admin.site.register(UserInfo)
admin.site.register(Tag)
admin.site.register(UserFans)
admin.site.register(Blog)