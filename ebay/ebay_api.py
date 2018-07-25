import json

from django.conf import settings
from ebaysdk.trading import Connection as Trading
from datetime import date, datetime
# from .slackapi import send_notification

API_MAP = dict()

api = Trading(
    appid=settings.APP_ID,
    devid=settings.DEV_ID,
    certid=settings.CERT_ID,
    token=settings.TOKEN,
    config_file=None,
    domain=settings.DOMAIN
)


def register(api_name):
    def wrapper(api_function):
        API_MAP[api_name] = api_function
        return api_function
    return wrapper


@register('GetMyeBaySelling')
def get_my_ebay_selling(data):
    page_no = data.get('page_no')
    response = api.execute('GetMyeBaySelling', {
        'ActiveList': {
            'Include': 'true',
            'Pagination': {
                'EntriesPerPage': '200',
                'PageNumber': page_no,
            }
        }
    })
    return response


@register('GetSellerList')
def get_seller_list(data):
    end_time_from = date.today()
    end_time_to = date(end_time_from.year, end_time_from.month + 3, end_time_from.day)
    page_no = data.get('page_no')
    response = api.execute('GetSellerList', {
            # 'DetailLevel': 'ReturnAll',
            'GranularityLevel': 'Fine',
            'EndTimeFrom': str(end_time_from),
            'EndTimeTo': str(end_time_to),
            'Pagination': {
                'EntriesPerPage': '200',
                'PageNumber': page_no,
            }
    })
    return response


@register('ReviseItem')
def revise_item(data):
    response = api.execute('ReviseItem', {
        'Item': {
            'ItemID': data.get('item_id'),
            'Title': data.get('title'),
            'StartPrice': data.get('price'),
        }

    })
    return response


@register('EndItem')
def end_item(data):
    response = api.execute('EndItem', {
        'ItemID': data.get('item_id'),
        'EndingReason': 'NotAvailable',
    })
    return response


@register('SetNotificationPreferences')
def set_notification_references(data):
    response = api.execute('SetNotificationPreferences', {
        'UserDeliveryPreferenceArray': {
            'NotificationEnable': {
                'EventType': data.get('event_type'),
                'EventEnable': data.get('event_enable')
            }
        }
    })
    return response


@register('SetNotificationURL')
def set_notification_url(data):
    response = api.execute('SetNotificationPreferences', {
        'ApplicationDeliveryPreferences': {
            'ApplicationURL': data.get('url')
        }
    })
    return response


@register('GetNotificationPreferences')
def get_notification_references(data):
    response = api.execute('GetNotificationPreferences', {
        'PreferenceLevel': 'User',
    })
    return response


@register('GetNotificationURL')
def get_notification_url(data):
    response = api.execute('GetNotificationPreferences', {})
    return response


@register('GetItem')
def get_item(data):
    response = api.execute('GetItem', {
        'ItemID': data.get('item_id')
    })
    return response


@register('GetSellingManagerSoldListings')
def get_selling_manager_sold_listings(data):
    response = api.execute('GetSellingManagerSoldListings', {
        'Pagination': {
            'EntriesPerPage': '200',
            'PageNumber': data.get('page_no'),
        },
        'SaleDateRange': {
            'TimeFrom': str(date.today()) + "T00:00:00.000Z",
            'TimeTo': datetime.now(),
        },
        # 'Search': {
        #     'SearchType': 'ItemID',
        #     'SearchValue': '222595638759',
        # }

    })
    return response


@register('ReviseInventoryStatus')
def revise_inventory_status(data):
    revise_item_list = data['revise_item_list'][settings.EBAY]
    api_dict = dict()
    api_dict.update({'InventoryStatus': [i for i in revise_item_list]})
    response = api.execute('ReviseInventoryStatus', api_dict)
    return response


@register('ReviseItemDescription')
def revise_item_description(data):
    response = api.execute('ReviseItem', {
        'Item': {
            'ItemID': data.get('item_id'),
            'Description': data.get('description'),
        }

    })
    return response

