from django.contrib import admin
from .models import User, Post, PostLike, PostComment, UserFollow, Activity 


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_staff', 'is_active')


admin.site.register(User, CustomUserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_email', 'created_at', 'updated_at')

    def user_email(self, obj):
        return obj.user.email if obj.user else "No User"
    user_email.short_description = 'User Email'


admin.site.register(Post, PostAdmin)


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'user_email')

    def post_title(self, obj):
        return obj.post.title if obj.post else "No Post"
    post_title.short_description = 'Post Title'

    def user_email(self, obj):
        return obj.user.email if obj.user else "No User"
    user_email.short_description = 'User Email'


admin.site.register(PostLike, PostLikeAdmin)


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'user_email', 'comment_text', 'created_at')

    def post_title(self, obj):
        return obj.post.title if obj.post else "No Post"
    post_title.short_description = 'Post Title'

    def user_email(self, obj):
        return obj.user.email if obj.user else "No User"
    user_email.short_description = 'User Email'


admin.site.register(PostComment, PostCommentAdmin)


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'follows_email')

    def user_email(self, obj):
        return obj.user.email if obj.user else "No User"
    user_email.short_description = 'User Email'

    def follows_email(self, obj):
        return obj.follows.email if obj.follows else "No Followed User"

    follows_email.short_description = 'Follows Email'


admin.site.register(UserFollow, UserFollowAdmin)



@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_action_type', 'post', 'target_user', 'timestamp')

    def get_action_type(self, obj):
        return obj.get_action_type_display()

    get_action_type.admin_order_field = 'action_type'
    get_action_type.short_description = 'Action Type'