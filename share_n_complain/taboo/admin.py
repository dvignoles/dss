from django.contrib import admin

from .models import TabooWord


def add_to_taboo(admin, request, queryset):
	queryset.update(is_taboo=True)
add_to_taboo.short_description = "Add to taboo list"

def remove_from_taboo(admin, request, queryset):
	queryset.update(is_taboo=False)
remove_from_taboo.short_description = "Remove from taboo list"

class TabooWordAdmin(admin.ModelAdmin):
	#model = TabooWord
	list_display = ('word', 'suggested_by', 'is_taboo')
	actions = [add_to_taboo, remove_from_taboo]

admin.site.register(TabooWord, TabooWordAdmin)