import re
from datetime import datetime, timedelta
import dateutil.parser as dp

def clean_price(text):
    if not text:
        return None
    return re.sub(r"[^\d.]", "", text)

def parse_date(text):
    if not text:
        return None
    try:
        d = dp.parse(text)
        return d.strftime("%Y-%m-%d")
    except:
        return None

def compute_warranty_end(start_date, months):
    if not start_date or not months:
        return None
    dt = datetime.strptime(start_date, "%Y-%m-%d")
    year = dt.year + (dt.month + months - 1) // 12
    month = (dt.month + months - 1) % 12 + 1
    day = dt.day
    return f"{year:04d}-{month:02d}-{day:02d}"
