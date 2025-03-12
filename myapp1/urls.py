from django.contrib import admin
from django.urls import path
from.import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',include('myapp1.urls')),
    path('',views.home),
    path('about',views.about),
    path('contact',views.contact),
    path('book',views.book),
    path('register',views.register),
    path('login',views.login),
    path('dashboard',views.dashboard),
    path('logout',views.logout),

    path('save',views.save),
    path('check',views.check),
    path('savebook',views.savebook),
    path('payment',views.payment),
    path('editprofile',views.editprofile),
    path('saveeditprofile',views.saveeditprofile),

    path('forget',views.forget),
   # path('change',views.change),
    path('verify_otp',views.verify_otp),
    path('send_otp',views.send_otp),
    path('reset_password',views.reset_password),
    path('savemsg',views.savemsg),

    path('excel',views.excel),

]