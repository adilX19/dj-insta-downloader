from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.conf import settings
from datetime import datetime
import requests
import os

def get_video_url(url):
    response = requests.get(url)
    string = str(response.content)

    if "contentUrl" in string:
        content_list = string.split("contentUrl")[-1]
    else:
        print("Video Link not founded")
        return None

    url = content_list.split(':"')[1]
    url = url.replace("\\\\", "")
    url = url.split(',')[0]
    url = url.replace('"', '')
    url = url.replace('u0025', '%')
    return url

def prepare_video(url):
    resp = requests.get(url)
    file_str = str(datetime.now().timestamp()).replace('.', '_')
    filename = f"{file_str}_video.mp4"
    video_path = f'{settings.BASE_DIR}\\static\\media\\videos\\{filename}'

    with open(video_path, 'wb') as video_file:
        video_file.write(resp.content)
        return True, filename

def social_downloader_page(request):
    return render(request, "social_downloader.html", {})


def download_video(request, filename):

    print("Filename ==>", filename)

    video_path = f'{settings.BASE_DIR}\\static\\media\\videos\\{filename}'

    if os.path.exists(video_path):
        video_file = open(video_path, 'rb')
        response = FileResponse(video_file, content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return None

def start_video_download(request):
    prepared = False
    filename = ""

    query = request.GET.get("query", None)
    if query:
        url = get_video_url(query)
        prepared, filename = prepare_video(url) if url else (False, "")

    return JsonResponse({
        "prepared": prepared,
        "message": "File is prepared, please download it",
        "filename": filename
    })