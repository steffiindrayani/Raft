from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import requests
import simplejson

'const'
SELF_PORT = 9001
PORT_WORKER = 13337

class NodeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            self.send_response(200)

            self.send_header('Content-type','text/html')
            self.end_headers()
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            self.end_headers()
            data = simplejson.loads((self.data_string))
            JsonType = data['JsonType']
            print("Message received. JsonType : " + JsonType)
            self.send_response(200)

            if JsonType == 'CLIENT_REQUEST': #Kalau Json Type yang diterima adalah dari Client.....        
                PrimeRequest = data['PrimeRequest']
                print("CLIENT IS REQUESTING PRIME NUMBER: " + str(PrimeRequest))
                # self.wfile.write(str(PrimeRequest).encode('utf-8'))                
                # NUMB_JSON = simplejson.dumps({'JsonType':'NODE_REQUEST', 'PrimeRequest': + PrimeRequest})
                # r = requests.get("http://localhost:" + str(PORT_NODE), data=NUMB_JSON)
                url = "http://localhost:" + str(PORT_WORKER) + "/" + str(PrimeRequest)
                r = requests.get(url)
                if r.status_code == 200:
                    self.send_response(200)
                    answer = r.text
                    print(r.text)
                    self.wfile.write(str(r.text).encode('utf-8'))                
                else:
                    self.send_response(500)
                    self.wfile.write(str(-1).encode('utf-8'))                                    

        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

print('----- NODE -----')
print('SELF_PORT : ' + str(SELF_PORT))
server = HTTPServer(("", SELF_PORT), NodeHandler)
server.serve_forever()