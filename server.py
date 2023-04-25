import json
from http.server import BaseHTTPRequestHandler, HTTPServer
# Import this stdlib package first
from urllib.parse import urlparse, parse_qs
from views import get_all_metals, get_all_orders, get_all_sizes, get_all_styles, get_single_metal, get_single_order, get_single_style, get_single_size, create_order, update_order, delete_order, create_metal, create_size, create_style, update_metal, delete_metal, delete_size, delete_style, update_size, update_style
from repository import all, update, delete, create, retrieve

method_mapper = {
    "metals": {
        "single": get_single_metal,
        "all": get_all_metals,
        "create": create_metal,
        "delete": delete_metal,
        "update": update_metal
    },
    "styles": {
        "single": get_single_style,
        "all": get_all_styles,
        "create": create_style,
        "delete": delete_style,
        "update": update_style
    },
    "sizes": {
        "single": get_single_size,
        "all": get_all_sizes,
        "create": create_size,
        "delete": delete_size,
        "update": update_size
    },
    "orders": {
        "single": get_single_order,
        "all": get_all_orders,
        "create": create_order,
        "delete": delete_order,
        "update": update_order
    } 
}



class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = parse_qs(url_components.query)
        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass

        print(query_params)
        
        return (resource, id, query_params)

    def get_all_or_single(self, resource, id, query_params):
        if id is not None:
            response = retrieve(resource, id, query_params)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = all(resource)

        return response

    def do_GET(self):
        response = None
        (resource, id, query_params) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id, query_params)
        self.wfile.write(json.dumps(response).encode())




    def create_func(self, resource):
        """Function that dried up all the similar code in do_POST"""
        new_object = None
        if resource == "styles" or resource == "sizes" or resource == "metals":
            self._set_headers(405)
            new_object = {
                "message": f'{"This cannot be changed by you"}'
            }
            self.wfile.write(json.dumps(new_object).encode())

    def do_POST(self):
        """This CREATES a new object"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)
        (resource, id, query_params) = self.parse_url(self.path)

        new_order = None
        if resource == "orders":
            new_order = create_order(post_body)
            self.wfile.write(json.dumps(new_order).encode())
        else: 
            self.create_func(resource)




    def update_func(self, resource):
        if resource == "orders" or resource == "sizes" or resource == "styles":
            self._set_headers(405)

    def do_PUT(self):
        """This UPDATES the object"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        if resource == "metals":
            update_metal(id, post_body)
        else:
            self.update_func(resource)
        
        self.wfile.write("".encode())




    def delete_func(self, resource):
        if resource == "orders" or resource == "styles" or resource == "metals" or resource == "sizes":
            self._set_headers(405)
            # resource = {
            #     "message": f'{"Deleting requires you to contact company directly"}'
            # }
            self.wfile.write("".encode())

    def do_DELETE(self):
        """This DELETES the object"""
        (resource, id, query_params) = self.parse_url(self.path)

        self.delete_func(resource)
        self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()



# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
