import requests
from urllib.parse import urlparse 

Apache_Type = ["text/plain", "text/plain; charset=ISO-8859-1", 
                "text/plain; charset=iso-8859-1", 
                "text/plain; charset=UTF-8"]

check_for_apache = False

#handling resource metadata
def _get_resource_metadata(body, ContentType, http_origin):
    if http_origin:
        # resource retrieved via HTTP

        # TODO (Handle multiple Contentype headers)
        
        if ContentType in Apache_Type:
            check_for_apache = True
        
    return ContentType


#main function
def xtractmime(body: bytes, content_type: List[Union[str, bytes]], http_origin: bool, no_sniff: bool) -> str:
    supplied_type = _get_resource_metadata(body, ContentType, http_origin)

    pass

# SAMPLE INPUT
if __name__ == '__main__':
    
    url = "https://www.ecb.europa.eu/pub/pdf/other/developmentstatisticsemu200406en.pdf"
    response = requests.get(url)
    body = response.content
    ContentType = response.headers["Content-Type"]
    
    http_origin = False
    if urlparse(url).scheme in ('http', 'https'):
        http_origin = True
    #mimetype = xtractmime(body, ContentType, http_origin, False) #assuming sniffing allowed (no-sniff=False)
