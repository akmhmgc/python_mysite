from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# モデルのインポート
from .models import Choice, Question


# Create your views here.
def index(request):
    # 　モデルの読み込み
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # テンプレート内で使用する変数（コンテクスト）の設定
    context = {'latest_question_list': latest_question_list}
    # レンダリング
    return render(request, 'polls/index.html', context)


# getメソッドを用いた値の受け渡し
def show(request):
    text = str(request.GET['text'])
    return render(request, 'polls/show.html', {"text": text})


# テーブルが見つからなかった場合404を返す
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    # 対象の質問を変数に入れる
    question = get_object_or_404(Question, pk=question_id)
    try:
        # POSTデータから、選んだ質問を取り出し
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    # 例外が出なかった場合に実行される処理
    else:
        # choiceテーブルのvoteカラムに値を追加>更新
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
