from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from xml.etree.ElementTree import Element, SubElement, tostring
import json


class JsonToXmlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.headers.get('Format') == 'xml' and response.status_code == 200:
            data = {'data': response.data}
            root = Element('response')
            self._build_xml(root, data)
            xml_str = tostring(root, encoding='utf-8')
            return HttpResponse(xml_str, content_type='application/xml')
    
        return response

    def _build_xml(self, element, data):
        if isinstance(data, dict):
            for key, value in data.items():
                sub_element = SubElement(element, key)
                self._build_xml(sub_element, value)
        elif isinstance(data, list):
            for item in data:
                item_element = SubElement(element, 'item')
                self._build_xml(item_element, item)
        else:
            element.text = str(data)

    def process_request(self, request):
        print('Request headers:', request.headers)
        if request.headers.get('Content-Type') == 'application/xml':
            request.data = json.loads(json.dumps(request.data))
        return None
    
    def process_exception(self, request, exception):
        print('Exception:', exception)
        return None
    
    def process_template_response(self, request, response):
        print('Template response:', response)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        print('View function:', view_func)
        return None
