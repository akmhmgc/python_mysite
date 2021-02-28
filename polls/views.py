from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


# Create your views here.
class IndexView(generic.ListView):
    # デフォルトではないテンプレート名を指定する(デフォルトは<app name>/<model name>_list.html)
    template_name = 'polls/index.html'

    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # pub_dateが未来の日付のデータは返さない
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).exclude(choice=None).order_by('-pub_date')[:5]


# getメソッドを用いた値の受け渡し
def show(request):
    if "text" in request.GET:
        text = str(request.GET['text'])
    else:
        text = "default"
    return render(request, 'polls/show.html', {"text": text})


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        子モデル(choice)が存在しないものは除外
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(choice=None)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


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
