from django.contrib import admin

from .models import Document,Complaints_Owner


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

#transfer ownership of doc to the admin && set resolved to True
def take_ownership(admin, request, queryset):
	pass

#Set Resolved to True
def dismiss_complaint(admin, request, queryset):
	pass

class Complaints_OwnerAdmin(admin.ModelAdmin):
	list_display = ['doc_id','owner','complainer']
	actions = [take_ownership,dismiss_complaint]


admin.site.register(Document, DocumentAdmin)
admin.site.register(Complaints_Owner, Complaints_OwnerAdmin)