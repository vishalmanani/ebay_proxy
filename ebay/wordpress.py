import MySQLdb
from django.conf import settings


db_args = {
    # 'db': settings.EBAY,
    'db': 'ebay20',
    'user': 'root',
    'passwd': 'gu60pzr24365',
    'host': '52.211.97.99'
}


def update_for_revise(ebay_id, title, price):
    db = MySQLdb.connect(**db_args)
    cur = db.cursor()
    sql = "UPDATE ebay20_ebay_auctions " \
          "SET auction_title = '{title}'," \
          "price = '{price}' " \
          "WHERE  ebay_id ='{ebay_id}'".format(title=title, price=price, ebay_id=ebay_id)
    cur.execute(sql)
    db.commit()
    db.close()


def update_for_inventory_status(revise_item_list):
    db = MySQLdb.connect(**db_args)
    cur = db.cursor()
    for i in revise_item_list:
        sql = "UPDATE ebay20_ebay_auctions \
              SET price = '{price}' \
              WHERE  ebay_id ='{ebay_id}'".format(price=i.get('StartPrice'), ebay_id=i.get('ItemID'))
        cur.execute(sql)
    db.commit()
    db.close()


if __name__ == '__main__':
    update_for_revise('223075084073', 'Waterproof Android Smart Watch M26 Anti-lost Pedometer Men Woman Bluetooth V4.2', '150.00')
    update_for_inventory_status([{'ItemID': '223075084073', 'StartPrice': '152.00'}])