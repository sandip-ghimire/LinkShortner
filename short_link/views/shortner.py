from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .serializers import UrlSerializer
from .models import Urls
from http import HTTPStatus
from .errors import NOT_FOUND
import hashlib
import uuid


@api_view(['POST'])
def encode_url(request) -> JsonResponse:
    """
    Receives post request with long url.
    Shorten the url and adds it to the cache.
    Returns JsonResponse with short url.
    """
    serializer = UrlSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    url = serializer.data['url']
    response = {}
    short_url = get_short_url(url)
    response['url'] = short_url
    return JsonResponse(response, status=HTTPStatus.OK)


@api_view(['POST'])
def decode_url(request) -> JsonResponse:
    """
    Receives post request with short url.
    Search for the its corresponding long url in db.
    Returns JsonResponse with long url if found else returns 404 error.
    """
    serializer = UrlSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    url = serializer.data['url']
    response = {}
    try:
        long_url = Urls.objects.get(short_url=url).long_url
    except ObjectDoesNotExist:
        response['error'] = NOT_FOUND
        return JsonResponse(response, status=HTTPStatus.NOT_FOUND)

    response['url'] = long_url
    return JsonResponse(response, status=HTTPStatus.OK)


def get_short_url(long_url: str) -> str:
    """
    Helper function to get short url from provided long url.
    Scans for the long url in db, if available returns its short url.
    If not already created, it creates short urls and returns it.
    """
    check_dup = True
    short_url, code = generate_short_url(long_url)
    while check_dup:
        db_record = Urls.objects.filter(short_url=short_url)
        if db_record.exists():
            if long_url == db_record[0].long_url:
                return short_url
            else:
                short_url, code = generate_random_short_url(long_url)
        else:
            check_dup = False

    Urls.objects.create(id=code, short_url=short_url, long_url=long_url)
    return short_url


def generate_short_url(long_url: str) -> tuple:
    """
    Creates sha256 hex code for provided long url.
    Trims the length as per pre defined max length.
    Appends hex code to pre-url and add it to the cache.
    """
    hash_obj = hashlib.sha256(long_url.encode())
    hex_code = hash_obj.hexdigest()
    short_code = hex_code[:int(settings.HEX_CODE_LENGTH)]
    short_url = '{0}/{1}'.format(settings.PRE_URL, short_code)
    return short_url, short_code


def generate_random_short_url() -> tuple:
    """
    Creates random hex code using uuid.
    Trims the length as per pre defined max length.
    Appends hex code to pre-url and add it to the cache.
    """
    short_code = uuid.uuid4().hex[:int(settings.HEX_CODE_LENGTH)]
    short_url = '{0}/{1}'.format(settings.PRE_URL, short_code)
    return short_url, short_code
