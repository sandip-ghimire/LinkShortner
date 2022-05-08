"""ShortLink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

"""
from django.contrib import admin
from django.urls import path
from .views import shortner, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.landing_page, name='home'),
    path('statistics', home.statistics, name='statistics'),
    path('count', home.count, name='count'),
    path('delete', home.delete, name='delete'),
    path('encode', shortner.encode_url, name='encode_shortlink'),
    path('decode', shortner.decode_url, name='decode_shortlink'),
]
