from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)


from models import Question, Survey, Theme,CompanyDetail,Mail,Response,AnswerBase,AnswerRadio
from forms import ResponseForm
from django.views import generic
from django.shortcuts import get_object_or_404
from mail_templated import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import urllib
from chartit import DataPool, Chart
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Sum,Count
from chartit import PivotDataPool, PivotChart
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt



def brodcastsurvey(request):
        template_name = 'survey/broadcast.html'
        ID= Survey.objects.latest('id')
        companydetails=CompanyDetail.objects.all()

        contex={
        'companydetails':companydetails,
        'surveyname':ID.name,
        }
        return render(request, template_name,contex)




def Index(request):
            total_response = Response.objects.all().count()
            survey = Survey.objects.all()
            active_survey=Survey.objects.filter(active=True)
            companydetails =CompanyDetail.objects.all()
            contex={
            'companydetails':companydetails,
            'survey':survey,
            'activesurvey':active_survey,
            'total_resp':total_response,
            }

            return render(request, 'home.html',contex)

def SurveyDetail(request, id):
            companydetails =CompanyDetail.objects.all()
            survey = Survey.objects.get(id=id)
            category_items = Theme.objects.filter(survey=survey)
            categories = [c.name for c in category_items]
            print 'themes for this survey:'
            print categories
            if request.method == 'POST':
		form = ResponseForm(request.POST, survey=survey)
		if form.is_valid():
			response = form.save()
			return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
            else:
		form = ResponseForm(survey=survey)
		print form
		# TODO sort by category

            return render(request, 'survey.html', {'response_form': form, 'survey': survey, 'categories': categories,  'companydetails':companydetails})

def Confirm(request, uuid):
            companydetails =CompanyDetail.objects.all()
            contex={
            'companydetails':companydetails,
            }

            email = settings.support_email
            return render(request, 'confirm.html', {'uuid':uuid, "email": email},contex)

def privacy(request):
        companydetails =CompanyDetail.objects.all()
        contex={
        'companydetails':companydetails,
        }
        return render(request, 'privacy.html',contex)

def sendsms(request):
    # Specify your login credentials
        for user in Mail.objects.all():
                username = "adamz78"
                apikey   = "eb8c8297fddbbc6104ffc379a64170085fc6e6e1921a7165f83ae83402546918"

                # Please ensure you include the country code (+254 for Kenya in this case)
                to      = "+254702357053"
                ID= Survey.objects.last()
                getvars=ID.id
                url='http://oroni.pythonanywhere.com/survey/'



                message ="You have received this sms in order to participate  in  a  survey  \nThe survey  is  very brief and will only take  about 5 minutes tocomplete.   Please  click the link below to  go  to  the survey website .Your pass code :  "+str(user.user_uuid)+'   link' + url+str(getvars)

                # Create a new instance of our awesome gateway class
                gateway = AfricasTalkingGateway(username, apikey)

                try:
                    # Thats it, hit send and we'll take care of the rest.

                    results = gateway.sendMessage(to, message)

                    for recipient in results:
                        # status is either "Success" or "error message"
                        print 'number=%s;status=%s;messageId=%s;cost=%s' %(recipient['number'],
                                                                        recipient['status'],
                                                                        recipient['messageId'],
                                                                        recipient['cost'])
                except AfricasTalkingGatewayException, e:
                    print 'Encountered an error while sending: %s' % str(e)

        return render(request, 'privacy.html')





def sendemail(request):
        for address in Mail.objects.all():
            username = request.user
            url='http://oroni.pythonanywhere.com/survey/'

            plaintext = get_template('email/email.txt')
            htmly = get_template('email/email.html')
            ID= Survey.objects.last()
            getvars=ID.id
            d = Context({ 'username': username })
            text_content = 'This is an important message.'
            html_content = '<p>This is an <strong>important</strong> message. </p>\nYou are requested to participation   in  a   briefsurvey.The survey  is  very    brief   and will    only    take    about   5   minutes tocomplete.   Please  click   the link  below   to  go  to  the survey  Web site<br>\n'+ url+str(getvars)+'REMEMBER YOUR INVITE CODE'
            userpasscode=address.user_uuid
            subject='Survey Invite code '+str(userpasscode)
            from_email='testsurvey00012@gmail.com'

            to_emails = ['brianoroni6@gmail.com']
           # to_emails = [address.email]
            msg = EmailMultiAlternatives(subject, html_content, from_email, bcc=to_emails)
            msg.attach_alternative(html_content, "text/html")

            msg.send()
        return render(request, 'survey/mail_confirmation.html')


def analysis_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    total_response = Response.objects.all().count()

    companydetails =CompanyDetail.objects.all()
    surveys =Survey.objects.all()
    mails= Mail.objects.all()
    male_users= mails.filter(gender='Male').count()
    female_users= mails.filter(gender='Female').count()



    category_items = Theme.objects.filter(survey=surveys)
    categories = [c for c in category_items]


#==-----------------------------------------------------------------------------------------------------------------------------------------------------------


    #______________________---------------------------------------------------------------------------------------------------------------------


    responsedata =PivotDataPool(
                           series=[{
                                'options': {
                                'source': Response.objects.all(),
                                'categories': ['survey_id'],
                                'legend_by': 'survey',
                                'top_n_per_cat': 3,
                                },
                                'terms': {
                                'resp': Count('answerbase'),
                                }
                                }]
                                )

    #Step 2: Create the Chart object
    responsechart = PivotChart(
                datasource = responsedata ,
                series_options=[{
                                'options': {
                                'type': 'column',
                                'stacking': True
                                },
                                'terms': ['resp']
                                }],
                chart_options =
                {'title': {
                'text': 'Total Response Per Survey Question Analysis'},
                'xAxis': {
                'title': {
                'text': 'Survey'}}})


#----------------------------------------------------------------------------------------------------Pivot Data---------------------------------

# Step 1: Create a PivotDataPool with the data we want to retrieve.
    surveypivotdata = PivotDataPool(
                                series=[{
                                'options': {
                                'source': Survey.objects.all(),
                                'categories': ['name'],
                                'legend_by': 'name',
                                'top_n_per_cat': 1,
                                },
                                'terms': {
                                'avg_resp': Avg('response'),
                                }
                                }]
                                )
            # Step 2: Create the PivotChart object
    surveypivcht = PivotChart(
                            datasource=surveypivotdata,
                            series_options=[{
                                'options': {
                                'type': 'bar',
                                'stacking': True
                                },
                                'terms': ['avg_resp']
                                }],
                                chart_options={
                                'title': {
                                'text': 'Surveys Avarage Response'
                                },
                                'xAxis': {
                                'title': {
                                'text': 'Survey'
                                }
                                }
                                }
                                )
    #--------------------------------------------------------------------------Gender response----------------------------------------
    responsegender = PivotDataPool(
                           series=[{
                                'options': {
                                'source': Response.objects.all(),
                                'categories': ['survey'],
                                'legend_by': 'survey',
                                'top_n_per_cat': 1,
                                },
                                'terms': {
                                'totalresponders': Count('user_uuid'),

                                }
                                }]
                                )
            # Step 2: Create the PivotChart object
    responsegenderpivcht = PivotChart(
                   datasource=responsegender,
                            series_options=[{
                                'options': {
                                'type': 'column',
                                'stacking': True
                                },
                                'terms': ['totalresponders']
                                }],
                                chart_options={
                                'title': {
                                'text': 'Surveys Avarage Response'
                                },
                                'xAxis': {
                                'title': {
                                'text': 'Survey'
                                }
                                }
                                }
                                )

    context={
        'companydetails':companydetails,
        'surveytotal':Survey.objects.all().count(),
        'total_resp':Response.objects.all().count(),
        'male':male_users,
        'female':female_users,
        'categories':categories,

        'chart_list' : [responsechart,surveypivcht,responsegenderpivcht],



    }

    #Step 3: Send the chart object to the template.
    return render(request,'survey/survey_analysis.html', context)

@require_GET
def show_survey_results(request):
    nores =AnswerRadio.objects.filter(body='No').count()
    yesres =AnswerRadio.objects.filter(body='Yes').count()

    context = {
        'noresponse': nores,
        'resresponse':yesres,
    }

    return render_to_response('survey/survey_result.html', context)







