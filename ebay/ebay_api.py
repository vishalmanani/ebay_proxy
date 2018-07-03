from django.conf import settings
from ebaysdk.trading import Connection as Trading
from datetime import date
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


@register('GetNotificationPreferences')
def get_notification_preferences(data):
    response = api.execute('GetNotificationPreferences', {
        'PreferenceLevel': 'User',
    })
    return response


# @register('GetOrders')
# def get_orders(data):
#     response = api.execute('GetOrders', {
#         'OrderIDArray': [
#             {
#                 'OrderID': '222037993704-2070296061012'
#             }
#         ]
#     })
#     return response
#
#
# @register('ReviseInventoryStatus')
# def revise_inventory_status(data):
#
#     item = data.get('item')
#     print('=========', item)
#     # item_id = data.get('ItemID', None)
#     # quantity = data.get('Quantity', None)
#     # sku = data.get('SKU', None)
#
#     # if item_id and quantity and sku:
#
#     ebay_response = api.execute('ReviseInventoryStatus', {
#         'InventoryStatus': item
#     })
#
#     if ebay_response.status_code == 200:
#         response = {
#             'status': 200,
#             'type': 'OK',
#             'message': 'ReviseInventoryStatus Api call',
#         }
#     else:
#         response = {
#             'status': 500,
#             'type': 'ERR',
#             'message': 'ReviseInventoryStatus API not call',
#         }
#         send_notification(str(ebay_response.json()), 'xpressbuyer')
#
#     # else:
#     #     response = {
#     #         'status': 500,
#     #         'type': 'ERR',
#     #         'message': 'ItemID,SKU or QTY not found in ReviseInventoryStatus',
#     #     }
#     #     send_notification('ItemID,SKU or QTY not found in ReviseInventoryStatus' + settings.EBAY, 'xpressbuyer')
#
#     return response


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
                'EntriesPerPage': '2',
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


@register('GetNotificationPreferences')
def get_notification_references(data):
    response = api.execute('GetNotificationPreferences', {
        'PreferenceLevel': 'User',
    })
    return response
