from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('storage/', views.DocumentListView.as_view()),
    path('add-doc/', views.AddDocumentView.as_view()),
    path('register/', views.UserRegisterView.as_view()),
    path('download-doc/<str:username>/<str:token>/<str:filename>/', views.DownloadDocView.as_view()),
    path('delete-doc/', views.DeleteDocumentView.as_view())

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)