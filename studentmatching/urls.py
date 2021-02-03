from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('profile/edit/', views.edit_profile),
    path('profile/view/', views.view_profile),
    path('profile/submit/', views.submit_profile),
    url(r'^users/(?P<username>[a-zA-Z0-9]+)/$', views.get_profile, name='user_by_name'),
    path('', include('social_django.urls', namespace='social')),
    path('messageboard/', views.MessageBoardCategoryIndex.as_view(), name='messageboard_category_index'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('messageboard/<int:pk>/', views.MessageBoardPostIndex.as_view(), name='category_post_index'),
    path('messageboard/<int:fk>/<int:pk>/', views.MessageBoardPostDetail.as_view(), name='messageboardpost_detail'),
    path('messageboard/makepost', views.make_post, name='make_post'),
    path('messageboard/createpost', views.MessageBoardPostCreate.as_view(), name='messageboardpost_create'),
    path('help/', views.help),
    path('search/', views.user_search_by_keyword, name='search'),
    path('messages/', views.view_messages, name='direct_messages'),
    url(r'^message/(?P<username>[a-zA-Z0-9]+)/$', views.send_message, name='send_message'),
    path('messages/delete/<int:pk>', views.delete_message, name='delete_message'),
    path('board_search/', views.board_search_by_keyword, name='board_search'),
]
