from django.urls import path
from .views import social_downloader_page, start_video_download, download_video

urlpatterns = [
	path('downloader/', social_downloader_page, name='social_downloader_page'),
	path('start/', start_video_download, name='start_video_download'),
	path('download/<filename>/', download_video, name='download_video'),
]