from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path
import Flow.views
import Authentication.views
import Chat.views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Flow.views.home, name='home'),
    path('search/', Flow.views.show_results, name='search'),
    path('Groups/', Chat.views.GroupPage, name='GroupPage'),
    path('api/create-room/<int:eId>/',Chat.views.create_room, name='create-room'),
    path('create_event/', Flow.views.createEvent, name='create_event'),
    #path('login/', Authentication.views.login, name='login'),
    path('login/', Authentication.views.CustomLoginView.as_view(), name='login'),
    path('event/<int:eId>/', Flow.views.show_event, name='event'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signin/', Authentication.views.register, name='signin'),
    path('GroupPage/', Chat.views.GroupPage, name='GroupPage'),
    path('Room_chat/<int:eId>/', Chat.views.Room_chat, name='Room_chat'),
    path('joinEvent/<int:eId>/', Flow.views.joinEvent, name='joinEvent'),
    path('JoinEventConfirm/<int:eId>/',Flow.views.JoinEventConfirm, name='JoinEventConfirm'),
    path('payment_cancel/', Authentication.views.payment_cancel, name='payment_cancel'),
    path('profile/', include('Authentication.urls')),
    path('update-like/', Flow.views.update_like, name='update-like'),
    path('member_profile/<int:id>/',
         Chat.views.member_profile, name='member_profile'),
    path('Roadmap/<int:eId>/',
         Chat.views.Roadmap, name='Roadmap'),
    #path('Roadmap_seeOnly/<int:eId>/',
     #    Flow.views.Roadmap_seeOnly, name='Roadmap_seeOnly'),    path('checkout/<int:event_id>/', Authentication.views.checkout, name='buy_ticket'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
