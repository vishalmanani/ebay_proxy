import json
import logging
import requests
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ebaysdk.exception import ConnectionError
from .ebay_api import API_MAP
from ebaysdk import response as res
from .slackapi import send_notification

slack_logger = logging.getLogger('django.request')


class EbayAPI(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EbayAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body.decode("UTF-8"))
            api_name = data.get('api')
            api_function = API_MAP.get(api_name, None)

            if api_function:
                response = api_function(data)
            else:
                response = {
                    'status': 500,
                    'ebay': settings.EBAY,
                    'message': api_name + ' API not register'
                }
                send_notification(api_name + ' API not registered in ' + settings.EBAY, 'xpressbuyer')

        except ConnectionError as e:
            slack_logger.error("eBay API ConnectionError " + settings.EBAY, exc_info=True)
            response = {
                'status': 500,
                'type': 'ERR',
                'message': 'ebay api connection error',
                'ebay': settings.EBAY,
            }
        except Exception as e:
            slack_logger.error("Error while call ebay API " + settings.EBAY, exc_info=True)
            response = {
                'status': 500,
                'type': 'ERR',
                'message': 'Internal Server Error',
                'ebay': settings.EBAY,
            }
        return JsonResponse(response)


class EbayWebHook(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EbayWebHook, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            xml = request.body
            rdo = res.ResponseDataObject({'content': xml})
            r = res.Response(rdo)
            data = r.json()

            notification_data = requests.post('http://127.0.0.1:8089/webhook/notification/', data=data)
            notification_data = notification_data.json()

            if notification_data.get('status') == 200:
                response = {
                    'status': 200,
                    'type': 'OK',
                    'message': 'Successfully Processed Notification',
                }
            else:
                response = {
                    'status': 500,
                    'type': 'ERR',
                    'message': 'Internal Server Error',
                }

        except Exception as e:
            slack_logger.error("Error while call ebay webhook " + settings.EBAY, exc_info=True)
            response = {
                'status': 500,
                'type': 'ERR',
                'message': 'Internal Server Error',
            }
        return JsonResponse(response, status=response.get('status'))
