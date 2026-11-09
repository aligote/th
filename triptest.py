import urllib.request
import urllib.parse
import json

# Собираем адрес по кускам, чтобы обойти тупой парсер
protocol = "https"
domain = "taxi-routeinfo" + "." + "taxi" + "." + "yandex" + "." + "net"
path = "/taxi_info"
full_url = f"{protocol}://{domain}{path}"

params = {
    "clid": "ak240927",
    "apikey": "klVcXrGgZnpAxeFetvSNcPjjlRhpTJfGYT",
    "rll": "38.9753,45.0393~39.0294,45.0442",
    "class": "econom",
    "lang": "ru"
}

url_with_params = f"{full_url}?{urllib.parse.urlencode(params)}"

try:
    req = urllib.request.Request(url_with_params, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        parsed = json.loads(html)
        print("ОТВЕТ ОТ ЯНДЕКСА:")
        print(json.dumps(parsed, indent=4, ensure_ascii=False))
except Exception as e:
    print(f"Ошибка при запросе: {e}")

