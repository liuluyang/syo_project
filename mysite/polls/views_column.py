from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse

from polls.models import Column, Column_child, Article


def article_list(request):

    all_column = Column.objects.all()
    print (all_column)
    data = {}
    for col in all_column:
        childs = col.column_child_set.all()
        data[col.name] = {'childs':childs}
        for art in childs:
            data[col.name]['articles'] = art.article_set.all()
    print (data)

    return render_to_response('article_list.html', locals())
