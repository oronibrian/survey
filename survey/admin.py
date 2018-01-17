from survey.models import BroadCast_Email,Mail,SurveyCompany, CompanyDetail,Question, Theme, Survey, Response,Department,AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple,AnswerBase
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User,Group
from django.core.mail import (send_mail,BadHeaderError,EmailMessage)
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.contrib.auth.models import User
import threading

from django.contrib import admin
from django.utils.safestring import mark_safe
import threading
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import (send_mail, BadHeaderError, EmailMessage)
from django.contrib.sites.models import Site
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin


class SurveyCompanyInline(admin.TabularInline):
            model =SurveyCompany
            extra=0
class QuestionInline(admin.TabularInline):
	model = Question
	ordering = ('category',)
	extra = 0

class CategoryInline(admin.TabularInline):
	model = Theme
	extra = 0

class SurveyAdmin(admin.ModelAdmin):
	inlines = [CategoryInline, QuestionInline]

class AnswerBaseInline(admin.StackedInline):
	fields = ('question', 'body')
	readonly_fields = ('question',)
	extra = 0

class AnswerTextInline(AnswerBaseInline):
	model= AnswerText

class AnswerRadioInline(AnswerBaseInline):
	model= AnswerRadio

class AnswerSelectInline(AnswerBaseInline):
	model= AnswerSelect

class AnswerSelectMultipleInline(AnswerBaseInline):
	model= AnswerSelectMultiple

class AnswerIntegerInline(AnswerBaseInline):
	model= AnswerInteger

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('interview_uuid', 'created')
	inlines = [AnswerTextInline, AnswerRadioInline, AnswerSelectInline, AnswerSelectMultipleInline, AnswerIntegerInline]
	# specifies the order as well as which fields to act on
	readonly_fields = ('survey', 'created', 'updated', 'interview_uuid')



#Sending batch emails
class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        try:
            msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

class BroadCast_Email_Admin(admin.ModelAdmin):
    model = BroadCast_Email

    def submit_email(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Mail.objects.all() ] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email.short_description = 'Submit BroadCast (1 Select Only)'
    submit_email.allow_tags = True

    actions = [ 'submit_email' ]

    list_display = ("subject", "created")
    search_fields = ['subject',]


# handle import export of data in all formats for Mail model
class MailResource(resources.ModelResource):

    class Meta:
        model = Mail
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('employeeid',)
        exclude = ('date_of_birth','start_date','end_date' )


    def for_delete(self, row, instance):
        return self.fields['name'].clean(row) == ''

class MailAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = MailResource
    readonly_fields = ['user_uuid']


#-------------------------------------------------------------------------------------

# handle import export of data in all formats for SurveyCompany model
class SurveyCompanyResource(resources.ModelResource):

    class Meta:
        model = SurveyCompany

class SurveyCompanyAdmin(ImportExportModelAdmin):
    resource_class = SurveyCompanyResource
#-------------------------------------------------------------------------------------



# Register all models

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(CompanyDetail)
admin.site.register(Department)
admin.site.register(Mail,MailAdmin)
admin.site.register(SurveyCompany,SurveyCompanyAdmin)
admin.site.register(AnswerBase)

# Unregistered models

admin.site.unregister(Site)
admin.site.unregister(Group)