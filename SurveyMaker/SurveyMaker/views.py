from django.views import View
from django.http import HttpResponse
from django.template import loader
from .models import Question, Option


def detail(request, question_id):
    return HttpResponse("Question: %s." % question_id)


def results(request, question_id):
    response = "Response for question %s:"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("Choose options for question %s." % question_id)


def viewQuestion(request, question_id):
    question = Question.objects.get(pk=question_id)
    options = Option.objects.filter(question=question_id)
    # question_list = Question.objects.order_by('-serial_number')[:5]
    template = loader.get_template('SurveyMaker/viewQuestion.html')
    context = {
        # 'question_list': question_list,
        'question': question,
        'options': options
    }
    return HttpResponse(template.render(context, request))
