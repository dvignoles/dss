from django.contrib import admin

from .models import Document


def unlock_doc(admin, request, queryset):
	queryset.update(locked=False)
unlock_doc.short_description = "Unlock Document"

class DocumentAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'private', 'locked')
	actions = [unlock_doc]

admin.site.register(Document, DocumentAdmin)