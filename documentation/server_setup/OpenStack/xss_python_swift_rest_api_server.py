# Uses Python3 http.server for serving requests
# Rodney Beede - 2025-09

#!!!!! IMPORTANT!!!!
# If using Python 3.13 or later you will need to install legacy-cgi
# https://pypi.org/project/legacy-cgi/
import cgi
#!!!!!!!!!

import http.server
import logging
import string
import sys
import urllib3

from swiftclient.service import SwiftService, SwiftError, SwiftUploadObject


def main(argv):

    # Quiet down the default logging
    logging.basicConfig(level=logging.ERROR)
    logging.getLogger("requests").setLevel(logging.CRITICAL)
    logging.getLogger("swiftclient").setLevel(logging.CRITICAL)
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    

    port = int(argv[1])  # port to listen on (http, no TLS)
    
    container = "fileuploads"

    # Assumes lab OpenStack Swift has been setup and running from same box
    swift_opts = {
        "auth_version": "1.0",
        "auth": "https://localhost:8888/auth/v1.0",
        "user": "system:root",
        "key": "testpass",
        "insecure": True
    }

    custom_handler = HandlerFactory(container, swift_opts)
    http_daemon = http.server.ThreadingHTTPServer(
        ("", port),  # All IPv6 or IPv4 interfaces
        custom_handler
    )
    
    http_daemon.serve_forever()
    

def HandlerFactory(container, swift_opts):
    class VulnerableObjectStorageHTTPRequestHandler(http.server.BaseHTTPRequestHandler, object):
        protocol_version = "HTTP/1.1"
        
        def __init__(self, *args, **kwargs):
            self.container = container
            self.swift_opts = swift_opts
            super(VulnerableObjectStorageHTTPRequestHandler, self).__init__(*args, **kwargs)


        def do_GET(self):
            print(f"Connection from f{self.client_address}")
            
            if(self.path == "/favicon.ico"):
                self.send_response(404)
                self.send_header("Content-Length", 0)
                self.end_headers()
                return

        
            response_content = "<html><body>"
            response_content += "<form action='/REST/API/endpoint.cgi' method='post' enctype='multipart/form-data'>"
            response_content += "Upload a file: <input type='file' name='file'/><input type='submit' />"
            response_content += "</form>"
            response_content += "<hr/>"
            response_content += "<h1>"
            response_content += "List of Uploaded Files"
            response_content += "</h1>"
            response_content += "<pre>"
            
            with SwiftService(options = self.swift_opts) as swift:
                try:
                    list_parts_gen = swift.list(container = self.container)
                    for page in list_parts_gen:
                        if page["success"]:
                            for item in page["listing"]:

                                i_size = int(item["bytes"])
                                i_name = item["name"]
                                i_etag = item["hash"]

                                response_content += f"{i_name} [size: {i_size}] [etag: {i_etag}]\r\n"
                        else:
                            raise page["error"]

                except SwiftError as e:
                    print(e.value)
            
            response_content += "</pre>"
            response_content += "</body></html>"


            encoded_response_content = response_content.encode("utf-8")

            self.send_response(200)
            self.send_header("Author", "rodneybeede.com")
            self.send_header("Content-Type", "text/html")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.send_header("Content-Length", len(encoded_response_content))
            self.end_headers()

            self.wfile.write(encoded_response_content)


        def do_POST(self):
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                })

            filename = form['file'].filename
            allowlist_chars = set((
                'a','b','c','d','e','f',
                'g','h','i','j','k','l',
                'm','n','o','p','q','r',
                's','t','u','v','w','x',
                'y','z','0', '1', '2',
                '3', '4', '5', '6', '7',
                '8', '9','.'
                ))
            if any(char not in allowlist_chars for char in filename):
                errmsg_encoded = f"You can only use filenames with characters {','.join(sorted(allowlist_chars))}".encode("utf-8")
                self.send_response(400)
                self.send_header('Content-Length', len(errmsg_encoded))
                self.send_header('X-Hint', 'Think outside of the web server box. Take a nice REST.')
                self.end_headers()
                self.wfile.write(errmsg_encoded)
                return

            #data = form['file'].file.read()
            
            with SwiftService(options = self.swift_opts) as swift:
                try:
                    for result in swift.upload(
                        container=self.container,
                        objects=[
                            #SwiftUploadObject(source=form['file'].file, object_name=filename),
                            SwiftUploadObject('/etc/passwd', object_name=filename),
                        ]):
                            if not 'success' in result:
                                print(result['error'])
                except SwiftError as e:
                    print(e.value)


                msg_encoded = f"File {filename} uploaded successfully".encode("utf-8")
                self.send_response(200)
                self.send_header('Content-Length', len(msg_encoded))
                self.end_headers()
                self.wfile.write(msg_encoded)


    # HandlerFactory
    return VulnerableObjectStorageHTTPRequestHandler  # factory return




if __name__ == "__main__":
    main(sys.argv)
