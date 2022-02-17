"""authentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from allauth.account.views import LoginView, SignupView
from django.contrib import admin
# from django.contrib.staticfiles.templatetags import staticfiles
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from . import views
# from django.templatetags.static import static

from user_profile.forms import ProfileSignupForm
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path(
        "",
        include(
            (
                [
                    path("", LoginView.as_view(), name="login"),
                    path("signup/",SignupView.as_view(form_class=ProfileSignupForm),name="signup",),
                    path("landing/",views.landing_page,name="landing"),
                ],
                "authsession",
            ),
            namespace="auth",
        ),
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path('owner-details/',include('deals.urls')),
    path('initial/',include('settings.urls')),
    
   
]

urlpatterns = urlpatterns + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns

from django.contrib import admin

admin.autodiscover()
admin.site.enable_nav_sidebar = False