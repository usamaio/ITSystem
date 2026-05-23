from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('admin/', admin.site.urls),

    # APP URLS
    path('', include('ITSystem.urls')),

    # DJANGO AUTH URLS
    path('accounts/', include('django.contrib.auth.urls')),

    # PASSWORD CHANGE
    path(

        'accounts/password_change/',

        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html'
        ),

        name='password_change'

    ),

    path(

        'accounts/password_change_done/',

        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),

        name='password_change_done'

    ),

]