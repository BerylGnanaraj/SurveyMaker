from django.db import models
from django.urls import reverse
import datetime
from django.conf import settings

# Source:https://docs.djangoproject.com/en/4.1/intro/tutorial02/#creating-models


class Survey(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    organization = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    jumble_questions = models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='SurveyCreatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='SurveyUpdatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return 'Survey {} is conducted by {} for the purpose: {}'.format(self.name,
                                                                         self.organization,
                                                                         self.description)


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    serial_number = models.PositiveIntegerField()
    display_text = models.CharField(max_length=500)
    description = models.CharField(max_length=200, default='')
    scramble_options = models.BooleanField(default=False)
    survey = models.ForeignKey(Survey, on_delete=models.DO_NOTHING)
    soft_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='QuesCreatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='QuesUpdatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.id, self.display_text)


class Option(models.Model):
    id = models.BigAutoField(primary_key=True)
    option_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    soft_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='OptionCreatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='OptionUpdatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.id, self.option_text)


class ResponseStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    survey = models.ForeignKey(Survey, on_delete=models.DO_NOTHING)
    is_complete = models.BooleanField(default=False)
    save_status = models.ForeignKey(Question, on_delete=models.PROTECT)
    soft_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='StatusCreatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='StatusUpdatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return 'User {}\'s status is {}'.format(self.user, self.is_complete)


class Response(models.Model):
    id = models.BigAutoField(primary_key=True)
    option = models.ForeignKey(Option, on_delete=models.DO_NOTHING)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    soft_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ResponseCreatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ResponseUpdatedBy',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return 'For question {}, the user {} has submitted option {}'.format(self.question.id,
                                                                             self.user.id,
                                                                             self.option.id)