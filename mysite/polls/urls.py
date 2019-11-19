#coding:utf8


from django.urls import path
from mysite.settings import MEDIA_ROOT
from django.conf.urls.static import static

from polls.views import index, user_get, upload, showImg
from polls.views_column import article_list
from polls import quantification


urlpatterns = [
    path('index', index, name='index'),
    path('user', user_get, name='user'),

    path('upload', upload),
    path('show', showImg),

    path('list', article_list),

    path('setting_data', quantification.setting_data_get)

]

urlpatterns += static('/media/', document_root=MEDIA_ROOT)


