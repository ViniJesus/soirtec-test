from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # output = ", ".join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # templete = loader.get_template("polls/index.html")
    # context = {
    #     "latest_question_list": latest_question_list,
    # }
    # return HttpResponse(templete.render(context, request))

    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)
# Create your views here.

def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id) 

    # try: 
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, "polls/index.html", {"question": question})


    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question}) 



def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def all_results(request):
    questions = Question.objects.all()  # Busca todas as perguntas
    return render(request, "polls/all_results.html", {"questions": questions})



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Se o usuário não selecionar uma opção, exibe a mesma página com um erro
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Você precisa escolher uma opção!"
        })
    
    # Incrementa o número de votos da opção escolhida
    selected_choice.votes += 1
    selected_choice.save()

    # Redireciona para a página de resultados após o voto
    return HttpResponseRedirect(reverse("results", args=(question.id,)))