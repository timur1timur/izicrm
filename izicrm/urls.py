from django.contrib.auth import views
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include
from main.forms import UserLoginForm
from main.views import home

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(template_name="registration/login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('designer/', include('main.urls', namespace='main')),
    path('manager/', include('manager.urls', namespace='manager')),
    path('izi/', include('common.urls', namespace='common')),
    path('markup/', include('markup.urls', namespace='markup')),
    path('director/', include('director.urls', namespace='director')),
    path('report/', include('report.urls', namespace='report')),

]
