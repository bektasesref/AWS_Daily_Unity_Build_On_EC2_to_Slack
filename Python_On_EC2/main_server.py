import json
import properties
import scm
import unity_builder
import slack_message_sender
from PlasticData import PlasticData
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #print(f"Received GET request:\nPath: {self.path}\nHeaders: {self.headers}\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'GET request received')
        if self.path == "/":
            scm.sync_scm()
            if unity_builder.build_project() == "success":
                slack_message_sender.upload_file("Manual triggered build")
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data_str = post_data.decode('utf-8')
        #print(f"Received POST request:\nHeaders: {self.headers}\nBody: {post_data_str}\n")

        try:
            plastic_data = PlasticData(post_data_str)

            self.send_response(200)
            self.end_headers()

            #print("Commit --->  " + plastic_data.content)
            branch_name_from_commit = scm.extract_branch_name_from_commit(plastic_data.content)
            print(f"New commit from : {plastic_data.user[0]} on branch: {branch_name_from_commit}. Gonna check if it's from {properties.checkInAccount} and branch is: {properties.checkInBranchName}")
            if plastic_data.user[0] == properties.checkInAccount and branch_name_from_commit == properties.checkInBranchName:
                scm.sync_scm()
                if unity_builder.build_project() == "success":
                    slack_message_sender.upload_file(plastic_data.content)
            else:
                print(f"New check-in detected on {branch_name_from_commit} branch. Not gonna build")

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON data')


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=properties.serverPort):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
