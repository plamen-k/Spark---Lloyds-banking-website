# Code written by Plamen Kolev

from django.shortcuts import render
from django.shortcuts import render_to_response
from Bank.views import baseDict
from help.models import StaticQuestion
from help.forms import FormQuestinForm
from django.template import RequestContext

# Create your views here.
def help_main(request):
    dictionary = baseDict(request)

    staticQuestions = StaticQuestion.objects.all()
    dictionary.update({
        "staticQuestions" : staticQuestions
    })

    if request.method == "POST":
        form = FormQuestinForm(request.POST)
        if form.is_valid():
            form.save()
            dictionary.update({
                "message": "Question has been submitted !"
            })
            return render_to_response("alert.html", dictionary)
    else:
        form = FormQuestinForm()

    dictionary.update({
        "form" : form,
    })

    return render_to_response("help/main_help_page.html", dictionary, context_instance=RequestContext(request))
