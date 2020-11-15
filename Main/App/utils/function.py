def get_min_price(keys):
    return keys.saleprice


def get_price_order_product(val):
    return val.get('detail_product').price * val.get('amount')
