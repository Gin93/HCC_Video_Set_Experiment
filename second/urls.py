"""second URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path , include
from learn import views as learn_views
from learn import views_afew as learn_views_afew



urlpatterns = [
#    path('', learn_views.test, name='test'),
    path('emojudgement', learn_views.index, name='emo_index'),
    path('emojudgement_intro', learn_views.intro_page, name='intro'),
    path('emojudgement_tips', learn_views.intro_page2, name='intro2'),
    path('emojudgement_Demo', learn_views.demo_page, name='demo'),
#    path('p003info.html', learn_views.info_collection_p1, name='info1'),
    path('emojudgement_p003info', learn_views.info_p1, name='info1'),
    path('emojudgement_p003collection', learn_views.info_p1_collection, name='info1collection'),
    path('emojudgement_p004', learn_views.p4, name='p4'),
#    path('emojudgeplaying', learn_views.playing, name='play'),
#    path('emojudgement_playing.html', learn_views.playing, name='play1'),
    path('emojudgement_playing', learn_views.playing, name='play2'),
    path('emojudgement_save_authenticity',learn_views.save_authenticity, name='save_au'),
    path('emojudgement_confidence', learn_views.confidence, name='confidence'),
    path('emojudgement_savecondifence',learn_views.savecondifence, name = 'savecondifence'),
    path('emojudgement_continueskip',learn_views.breakpage, name = 'skip'),
    path('emojudgement_survey2', learn_views.info_collection_p2, name ='info2'),
    path('emojudgement_addinfo2todatabase', learn_views.info2_add, name ='info2add'),
    path('emojudgement_Conclusion', learn_views.end, name ='end'),
    path('emojudgement_Conclusion/result', learn_views.result_display, name ='display_result'),
    path('emojudgement_database_admin', learn_views.databasedisplay, name ='display_result'),

    path('emojudgement_dataset', learn_views.choices, name='emo_index'),

    path('emojudgement_afew_display_choice', learn_views_afew.video_display_choice, name='emo_index'),

    path('emojudgement_afew_videoset_<int:videos_set>', learn_views_afew.initialization, name='emo_index'),
    path('emojudgement_AFEW_intro', learn_views_afew.intro_afew, name='emo_index'),
    path('emojudgement_afew_tips', learn_views_afew.intro_page2, name='intro2'),
    path('emojudgement_afew_Demo', learn_views_afew.demo_page, name='demo'),
    path('emojudgement_afew_p003info', learn_views_afew.info_p1, name='info1'),

    path('emojudgement_afew_p003collection', learn_views_afew.info_p1_collection, name='info1collection'),
    path('emojudgement_afew_p004', learn_views_afew.p4_afew, name='emo_index'),
    path('emojudgement_afew_p004_02', learn_views_afew.p4_02_afew, name='emo_index'),
    path('emojudgement_AFEW_play', learn_views_afew.playing_afew, name='emo_index'),
    path('emojudgement_afew_save_authenticity', learn_views_afew.save_authenticity_afew, name='emo_index'),
    path('emojudgement_afew_confidence', learn_views_afew.confidence_afew, name='emo_index'),
    path('emojudgement_afew_savecondifence', learn_views_afew.savecondifence_afew, name='emo_index'),
    path('emojudgement_afew_break',learn_views_afew.breakpage_afew, name = 'emo_break'),
    path('emojudgement_afew_break1',learn_views_afew.breakpage_afew_mixed, name = 'emo_break'),
    path('emojudgement_afew_survey2', learn_views_afew.info_collection_p2_afew, name='emo_index'),
    path('emojudgement_afew_addinfo2todatabase', learn_views_afew.info2_add_afew, name ='info2add'),
    path('emojudgement_afew_erq', learn_views_afew.erq_render_afew, name ='end'),   
    path('emojudgement_afew_erqcollection', learn_views_afew.erq_collection_afew, name ='end'),   
    path('emojudgement_afew_end', learn_views_afew.end_afew, name ='end'),  
   

    path('emojudgement_afew_database_admin1', learn_views_afew.databasedisplay1, name ='display_result'),
    path('emojudgement_afew_database_admin2', learn_views_afew.databasedisplay2, name ='display_result'),
    path('emojudgement_afew_database_admin', learn_views_afew.databasedisplay, name ='display_result'),
    path('emojudgement_afew_unit_test', learn_views_afew.unit_test, name ='display_result'),



#    path('add/', learn_views.add, name='add'),
    #指明了什么链接可以被解析，并且对应显示什么视图
    #
    #简单说，name 可以用于在 templates, models, views ……中得到对应的网址，
    #相当于“给网址取了个名字”，只要这个名字不变，网址变了也能通过名字获取到。
#    path('new_add/<int:a>/<int:b>/', learn_views.add2, name='add2'),
#    path('admin/', admin.site.urls),
#    path('add2/<int:a>/<int:b>/', learn_views.old_add2_redirect),
    #自动跳转到另一个

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

