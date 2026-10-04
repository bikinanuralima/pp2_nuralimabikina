import re
import json


# Read file
with open("/Users/nuralima/pp26/practice5/raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Find products and their prices
pattern = r"(?m)^\d+\.\n(.+)\n([\d,]+)\s+x\s+([\d\s]+,\d+)\n([\d\s]+,\d+)"

matches = re.findall(pattern, text)


products = []

for match in matches:
    name = match[0]
    quantity = float(match[1].replace(",", "."))
    unit_price = float(match[2].replace(" ", "").replace(",", "."))
    item_total = float(match[3].replace(" ", "").replace(",", "."))

    products.append({
        "name": name,
        "quantity": quantity,
        "unit_price": unit_price,
        "total": item_total
    })


# Total amount
total_match = re.search(
    r"ИТОГО:\s*\n?([\d\s]+,\d+)",
    text
)

total = float(
    total_match.group(1)
    .replace(" ", "")
    .replace(",", ".")
)


# Date and time
datetime_match = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
    text
)

date = datetime_match.group(1)
time = datetime_match.group(2)


# Payment method
payment_match = re.search(
    r"(Банковская карта):\s*\n?([\d\s]+,\d+)",
    text
)

payment_method = payment_match.group(1)


# Final structured data
receipt = {
    "products": products,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}


print(json.dumps(receipt, ensure_ascii=False, indent=4))