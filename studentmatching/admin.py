from django.contrib import admin
from .models import Profile, MessageBoardCategory, MessageBoardPost, Message, MessageSummary
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import F

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

@admin.register(MessageSummary)
class MessageSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/message_summary.html'
    date_hierarchy = 'date'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
        'sender': F('sender'),
        'receiver':F('receiver'),
        'content':F('content')
        }
        response.context_data['summary'] = list(
            qs
                .values('date')
        .annotate(**metrics)
            .order_by('date')
        )

        return response

class MessageBoardPostInline(admin.TabularInline):
    model = MessageBoardPost

#the MessageBoardAdmin is for editing posts using the messageboard categories as the parent model for the posts
class  MessageBoardAdmin(admin.ModelAdmin):
    inlines = [MessageBoardPostInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(MessageBoardCategory, MessageBoardAdmin)
admin.site.register(Message)
admin.site.register(MessageBoardPost)
