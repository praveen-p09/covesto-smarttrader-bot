from forex_python.converter import CurrencyRates

c = CurrencyRates()

def get_price_in_inr(price, currency):
    try:
        if currency != 'INR':
            return round(c.convert(currency, 'INR', price), 2)
    except:
        return None
