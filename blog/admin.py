from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Article,Category

#My actions
# admin.site.disable_action('delete_selected')

def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
            '%d مقاله منتشر شد.',
            '%d مقالات منتشر شدند.',
            updated,
    ) % updated, messages.SUCCESS)
make_published.short_description = "انتشار مقاله های انتخاب شده"
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
            '%d مقاله پیش نویس شد.',
            '%d مقالات پیش نویس شدند.',
            updated,
    ) % updated, messages.SUCCESS)
make_draft.short_description = "پیش نویس مقاله های انتخاب شده"


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=('position','title','parent','slug','status')
    list_filter=(['status'])
    search_fields=('title','slug')
    prepopulated_fields={'slug':('title',)}
admin.site.register(Category,CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','slug','thumbnail_tag','author','jpublish','is_special','status','category_to_str')
    list_filter=('publish','status','author')
    search_fields=('title','description')
    prepopulated_fields={'slug':('title',)}
    ordering=('status','-publish')
    actions = [make_published,make_draft]

    
admin.site.register(Article,ArticleAdmin)