from django.urls import path

urlpatterns = [
    path('discipline', ''),
    path('discipline/<slug:discipline>', ''),
    path('discipline/<slug:discipline>/event', ''),
    path('discipline/<slug:discipline>/event/<slug:event>', ''),

    path('meet', ''),
    path('meet/<slug:meet>', ''),
    path('meet/<slug:meet>/instance/<slug:instance>', ''),
    path('meet/<slug:meet>/instance/<slug:instance>/analysis', ''),
    path('meet/<slug:meet>/instance/<slug:instance>/competition/<slug:competition>', ''),

    path('entity', ''),
    path('entity/<slug:slug>', ''),
    path('entity/<slug:slug>/identity/<slug:id>', ''),
    path('entity/<slug:slug>/analysis', ''),


    path('venue', ''),
    path('venue/<slug:slug>', ''),
    path('venue/<slug:slug>/analysis', '')
    path('venue/<slug:slug>/course/<slug:course>/analysis', '')
]
