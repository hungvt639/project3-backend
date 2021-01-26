import math

def get_min_price(keys):
    return keys.saleprice


def get_price_order_product(val):
    promotion = val.get("promotion")
    num = val.get('product_detail').saleprice
    amount = val.get('amount')
    if promotion:
        values = 0
        if promotion.type:
            values = num - promotion.value
        else:
            val = math.ceil(num * promotion.value / 100)
            if promotion.max_value and val > promotion.max_value:
                values = num - promotion.max_value
            else:
                values = num - val
        if values > 0:
            return values * amount
        else:
            return 0
    else:
        return num * amount


