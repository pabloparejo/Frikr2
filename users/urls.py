from django.conf.urls import include, url
from users import views


urlpatterns = [
    url(r'^$', views.UsersView.as_view(), name="users"),
    url(r'^(?P<list_type>(followers|following))/(?P<pk>[0-9]+)$', views.UsersView.as_view(), name="follow_list_display"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', 'users.views.logout', name="logout"),
    url(r'^profile/(?P<pk>[0-9]+)?$', views.ProfileView.as_view(), name="profile"),
    url(r'^signup/$', views.SignupView.as_view(), name="signup"),
    url(r'^(?P<toggle>(follow|unfollow))/(?P<pk>[0-9]+)$', views.FollowView.as_view(), name="follow_toggle"),
]
