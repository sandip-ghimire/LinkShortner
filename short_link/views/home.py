from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from .models import Urls
from django.core.exceptions import ObjectDoesNotExist


def landing_page(request):
    response = render(request, 'short_link/home.html', {
        'url': settings.URL,
        'preurl': settings.PRE_URL
    })
    return response


def statistics(request):
    link_list = []
    url_objs = Urls.objects.all()
    for obj in url_objs:
        row = {'id': obj.id, 'link': obj.short_url, 'count': obj.click_count}
        link_list.append(row)

    response = render(request, 'short_link/statistics.html', {
        'url': settings.URL,
        'preurl': settings.PRE_URL,
        'link_list': link_list
    })
    return response


def count(request):
    link = request.POST.get("url")
    today = timezone.now()
    try:
        url_obj = Urls.objects.get(short_url=link)
        if (url_obj.click_date.date()-today.date()).days == 0:
            click_count = url_obj.click_count + 1
        else:
            click_count = 0
            url_obj.click_date = today

        url_obj.click_count = click_count
        url_obj.save()

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Invalid link!"})

    return JsonResponse({"success": "Success"})


def delete(request):
    link = request.POST.get("url")
    try:
        url_obj = Urls.objects.get(short_url=link)
        url_obj.delete()

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Error: Invalid link!"})

    return JsonResponse({"success": "Link deleted successfully!"})
