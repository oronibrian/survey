from django.conf.urls import  include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings
from.import views
from django.conf.urls.static import static
from django.views.generic import RedirectView



admin.autodiscover()

urlpatterns =[
    # Examples:
    url(r'^$', RedirectView.as_view(url='homepage/', permanent=True)),

    url(r'^homepage/$', views.Index, name='homepage'),
    url(r'^survey/(?P<id>\d+)/$', views.SurveyDetail, name='survey_detail'),
    url(r'^confirm/(?P<uuid>\w+)/$', views.Confirm, name='confirmation'),
    url(r'^privacy/$', views.privacy, name='privacy_statement'),
    url(r'^sendsms/$', views.sendsms, name= 'sendsms'),
    url(r'^sendemail/$', views.sendemail, name= 'sendemail'),
    url(r'^brodcast/$', views.brodcastsurvey,name='brodcast'),
    url(r'^analysis/$', views.analysis_chart_view,name='analysis'),
    url(r'^result/$', views.show_survey_results,name='result'),








    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

 # Django JET URLS
    ]

admin.site.site_header ="Survey System Administration Centre"
admin.site.site_title= "survey system"


# media url hackery. le sigh.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
