from django.urls import path

urlpatterns = [
    path('sport/<slug:sport>/discipline', ''),
    path('sport/<slug:sport>/discipline/<slug:discipline>', ''),
    path('sport/<slug:sport>/discipline/<slug:discipline>/event', ''),
    path('sport/<slug:sport>/discipline/<slug:discipline>/event/<slug:event>', ''),

    path('sporting-event', ''),
    path('sporting-event/<slug:sporting-event>', ''),
    path('sporting-event/<slug:sporting-event>/<slug:competition>', ''),
    path('sporting-event/<slug:sporting-event>/<slug:competition>/analysis', ''),

    path('entity', ''),
    path('entity/<slug:slug>', ''),
    path('entity/<slug:slug>/identity/<slug:id>', ''),
    path('entity/<slug:slug>/analysis', ''),


    path('venue', ''),
    path('venue/<slug:slug>', ''),
    path('venue/<slug:slug>/analysis', ''),
    path('venue/<slug:slug>/course/<slug:course>/analysis', '')
]
