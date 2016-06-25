from django.conf.urls import url

from . import views

app_name = 'sparta'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^polls/(?P<pk>\d+)/fight-of-the-day/$', views.FightPollView.as_view(), name='fight-index'),
    url(r'^polls/(?P<pk>\d+)/performance-of-the-day/$', views.PerformancePollView.as_view(), name='performance-index'),
    url(r'^sparta-admin/$', views.SpartaAdminView.as_view(), name='sparta-admin'),
    url(r'^sparta-admin/polls$', views.PollsQuickView.as_view(), name='quick-view'),
    url(r'^sparta-admin/login$', views.LoginView.as_view(), name='login'),
    url(r'^sparta-admin/logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^events/manage/$', views.ManageEventsView.as_view(), name='manage-events'),
    url(r'^event/add/$', views.AddEventView.as_view(), name='add-event'),
    url(r'^event/(?P<pk>\d+)/update/$', views.UpdateEventView.as_view(), name='update-event'),
    url(r'^event/(?P<pk>\d+)/delete/$', views.DeleteEventView.as_view(), name='delete-event'),
    url(r'^fighters/manage/$', views.ManageFightersView.as_view(), name='manage-fighters'),
    url(r'^fighter/add/$', views.AddFighterView.as_view(), name='add-fighter'),
    url(r'^fighter/(?P<pk>\d+)/update/$', views.UpdateFighterView.as_view(), name='update-fighter'),
    url(r'^fighter/(?P<pk>\d+)/delete/$', views.DeleteFighterView.as_view(), name='delete-fighter'),
    url(r'^matches/manage/$', views.ManageMatchesView.as_view(), name='manage-matches'),
    url(r'^matches/add/$', views.AddMatchView.as_view(), name='add-match'),
    url(r'^matches/(?P<pk>\d+)/update/$', views.UpdateMatchView.as_view(), name='update-match'),
    url(r'^matches/(?P<pk>\d+)/delete/$', views.DeleteMatchView.as_view(), name='delete-match'),
]
