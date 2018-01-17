from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime, timedelta

from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models
import random


class CompanyDetail(models.Model):
    name = models.CharField(max_length=400)
    address = models.CharField(max_length=400)
    contact=models.IntegerField(default=1)


    def __unicode__(self):
        return (self.name)


class SurveyCompany(models.Model):
        name = models.CharField(max_length=200)
        address =models.CharField(max_length=400)
        description=models.TextField()

        def __unicode__ (self):
                return self.name
        class Meta:
                verbose_name_plural ='Survey companies'

class Department(models.Model):
        name = models.CharField(max_length=400)
        description = models.CharField(max_length=400)
        surveyowner =models.ForeignKey(SurveyCompany)


        def __unicode__(self):
             return (self.name)

class Survey(models.Model):
        active = models.BooleanField(default=False)
        name = models.CharField(max_length=400)
        description = models.TextField()
        surveyowner =models.ForeignKey(SurveyCompany)
        department = models.ManyToManyField(Department)
        publish = models.DateTimeField(auto_now=True, auto_now_add=False)
        enddate = models.DateTimeField(default=datetime.now()+timedelta(days=30))





        def __unicode__(self):
                return (self.name)

        def questions(self):
                if self.pk:
                        return Question.objects.filter(survey=self.pk)
                else:
                        return None


class Theme(models.Model):
        name = models.CharField(max_length=400)
        survey = models.ForeignKey(Survey)




        def __unicode__(self):
            return (self.name)
        class Meta:
                verbose_name='theme'
                verbose_name_plural ='Survey Themes'

def validate_list(value):
        '''takes a text value and verifies that there is at least one comma '''
        values = value.split(',')
        if len(values) < 2:
                raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")

class Question(models.Model):
        TEXT = 'text'
        RADIO = 'radio'
        SELECT = 'select'
        SELECT_MULTIPLE = 'select-multiple'
        INTEGER = 'integer'

        QUESTION_TYPES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (INTEGER, 'integer'),
        )

        text = models.TextField()
        required = models.BooleanField()
        category = models.ForeignKey(Theme, blank=True, null=True,)
        survey = models.ForeignKey(Survey)
        question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
        # the choices field is only used if the question type
        choices = models.TextField(blank=True, null=True,
        help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')

        def save(self, *args, **kwargs):
                if (self.question_type == Question.RADIO or self.question_type == Question.SELECT
                or self.question_type == Question.SELECT_MULTIPLE):
                        validate_list(self.choices)

                super(Question, self).save(*args, **kwargs)

        def get_choices(self):
            ''' parse the choices field and return a tuple formatted appropriately
            for the 'choices' argument of a form widget.'''
            choices = self.choices.split(',')
            choices_list = []
            for c in choices:
                    c = c.strip()
                    choices_list.append((c,c))
                    choices_tuple = tuple(choices_list)
            return choices_tuple

        def __unicode__(self):
                return (self.text)






class Mail(models.Model):
        GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),

        )

        name = models.CharField(max_length=300,blank=True, null=True)
        employeeid=models.CharField(max_length=200,primary_key=True)
        email = models.EmailField()
        date_of_birth= models.DateField(default=datetime.now(),blank=True)
        start_date=models.DateField(default=datetime.now(),blank=True)
        end_date=models.DateField(default=datetime.now(),blank=True)
        language =models.CharField(max_length=200,default='Eng')
        manager = models.CharField(max_length=200,default='Joseph')
        gender=models.CharField(max_length=200, choices=GENDER, default='Male')
        location=models.CharField(max_length=300,default='Nairobi')
        employment_type=models.CharField(max_length=300,blank=True,default='Full Time')
        department=models.CharField(max_length=255,null=True)
        user_uuid = models.IntegerField(default=random.randrange(1110),editable = False)








        def __unicode__(self):
          return self.name

        class Meta:
                verbose_name =' Employees '
                verbose_name_plural =' Staff Details '



class Response(models.Model):
# a response object is just a collection of questions and answers with a
# unique interview uuid
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        survey = models.ForeignKey(Survey)
        #interviewer = models.CharField('Name of Interviewer', max_length=400)
        user_uuid = models.IntegerField(default=1,blank=False)

        #conditions = models.TextField('Conditions during interview', blank=True, null=True)
        comments = models.TextField('Any additional Comments', blank=True,editable =True, null=True)
        interview_uuid = models.CharField("Interview unique identifier", max_length=36)

        def __unicode__(self):
                return ("response %s" % self.interview_uuid)

class AnswerBase(models.Model):
       question = models.ForeignKey(Question)
       response = models.ForeignKey(Response)
       created = models.DateTimeField(auto_now_add=True)
       updated = models.DateTimeField(auto_now=True)

# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
        body = models.TextField(blank=True, null=True)

class AnswerRadio(AnswerBase):
        body = models.TextField(blank=True, null=True)

class AnswerSelect(AnswerBase):
        body = models.TextField(blank=True, null=True)

class AnswerSelectMultiple(AnswerBase):
        body = models.TextField(blank=True, null=True)

class AnswerInteger(AnswerBase):
        body = models.IntegerField(blank=True, null=True)



class BroadCast_Email(models.Model):
        subject = models.CharField(max_length=200)
        created = models.DateTimeField(default=timezone.now)
        message = RichTextUploadingField(max_length=5000)

        def __unicode__(self):
            return self.subject

        class Meta:
            verbose_name = "BroadCast Email to all Member"
            verbose_name_plural = "BroadCast Email"
