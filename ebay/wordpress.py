import MySQLdb
from django.conf import settings


db_args = {
    # 'db': settings.EBAY,
    'db': 'ebay20',
    'user': 'root',
    'passwd': 'gu60pzr24365',
    'host': '52.211.97.99'
}


def update_for_revise(ebay_id, title, price, quantity):
    db = MySQLdb.connect(**db_args)
    cur = db.cursor()
    sql = "UPDATE ebay20_ebay_auctions " \
          "SET auction_title = '{title}'," \
          "price = '{price}'," \
          "quantity = '{quantity}'" \
          "WHERE  ebay_id ='{ebay_id}'".format(title=title, price=price, ebay_id=ebay_id, quantity=quantity)
    cur.execute(sql)
    db.commit()
    db.close()


def update_for_inventory_status(revise_item_list):
    when_stmt = ''
    ebay_id_list = []
    for i in revise_item_list:
        ebay_id_list.append(i.get('ItemID'))
        when_stmt += 'WHEN ebay_id = {ebay_id} THEN {price}'.format(ebay_id=i.get('ItemID'), price=i.get('StartPrice'))

    if len(ebay_id_list) == 1:
        for i in ebay_id_list:
            ebay_id_list = str("('" + i + "')")
    else:
        ebay_id_list = str(tuple(ebay_id_list))

    db = MySQLdb.connect(**db_args)
    cur = db.cursor()

    sql = "UPDATE ebay20_ebay_auctions \
          SET  price = CASE \
          {when_stmt}  \
          ELSE price \
          END  \
          WHERE  ebay_id in {ebay_id_list}".format(when_stmt=when_stmt, ebay_id_list=ebay_id_list)
    cur.execute(sql)
    db.commit()
    db.close()


def delete_for_end_listing(ebay_id):
    db = MySQLdb.connect(**db_args)
    cur = db.cursor()
    sql = "DELETE from ebay20_ebay_auctions WHERE ebay_id ='{ebay_id}'".format(ebay_id=ebay_id)
    cur.execute(sql)
    db.commit()
    db.close()


if __name__ == '__main__':
    update_for_revise('223075084073', 'Waterproof Android Smart Watch M26 Anti-lost Pedometer Men Woman Bluetooth V4.2', '150.00', '100')
    update_for_inventory_status([{'ItemID': '223075084073', 'StartPrice': '151.00'}])
    delete_for_end_listing('223075084073')
