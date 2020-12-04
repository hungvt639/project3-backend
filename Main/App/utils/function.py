def get_min_price(keys):
    return keys.saleprice


def get_price_order_product(val):
    return val.get('product_detail').saleprice * val.get('amount')


