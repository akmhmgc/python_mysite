from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# モデルのインポート
from .models import Question


# Create your views here.
def index(request):
    # 　モデルの読み込み
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # テンプレート内で使用する変数（コンテクスト）の設定
    context = {'latest_question_list': latest_question_list}
    # レンダリング
    return render(request, 'polls/index.html', context)


def show(request, user):
    return HttpResponse("あなたは{}番目の訪問者です".format(user))


# テーブルが見つからなかった場合404を返す
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
