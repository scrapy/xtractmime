# SAMPLE INPUT
import requests
from urllib.parse import urlparse 

url = "https://www.ecb.europa.eu/pub/pdf/other/developmentstatisticsemu200406en.pdf"

response = requests.get(url)
body = response.content

ContentType = response.headers["Content-Type"]

http_origin = False
if urlparse(url).scheme in ('http', 'https'):
    http_origin = True