from django.contrib import admin

from .models import Document


def unlock_doc(admin, request, queryset):
	queryset.update(locked=False)
unlock_doc.short_description = "Unlock Document"

class DocumentAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'private', 'locked')
	actions = [unlock_doc]

	def add_view(self,request,extra_content=None):
		self.exclude = ('collaborators','content','version', 'locked', 'locked_by', 'taboo_index')
		return super(DocumentAdmin,self).add_view(request)

	def change_view(self,request,object_id,extra_content=None):
		self.exclude = ('collaborators','content','version', 'taboo_index')
		return super(DocumentAdmin,self).change_view(request,object_id)

admin.site.register(Document, DocumentAdmin)