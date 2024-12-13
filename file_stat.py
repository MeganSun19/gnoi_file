# Save this as gnoi_stat.py in your gnoi_project directory

import grpc
from github.com.openconfig.gnoi.file import file_pb2, file_pb2_grpc
from grpc.beta import implementations

class UsernamePasswordCredentials(grpc.AuthMetadataPlugin):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __call__(self, context, callback):
        metadata = (
            ('username', self._username),
            ('password', self._password),
        )
        callback(metadata, None)

def perform_stat_operation(target, path, username, password):
    # Create channel credentials with username and password
    auth_creds = implementations.metadata_call_credentials(
        UsernamePasswordCredentials(username, password)
    )
    ca_cert= open('CA.cer', 'rb').read()
    channel_creds = grpc.ssl_channel_credentials(root_certificates=ca_cert)
    composite_creds = grpc.composite_channel_credentials(channel_creds, auth_creds)
    cert_cn = 'PE1-NCS57C3'
    options = (('grpc.ssl_target_name_override', cert_cn,),)
    # Create gRPC channel with composite credentials
    channel = grpc.secure_channel(target, composite_creds,options)
    # Create gNOI File service stub
    stub = file_pb2_grpc.FileStub(channel)
    # Create Stat request
    request = file_pb2.StatRequest(path=path)

    try:
        # Perform Stat RPC call
        response = stub.Stat(request)
        print(f"Stat response for {path}:")
        for stat in response.stats:
            print(f"Path: {stat.path}")
            print(f"Size: {stat.size} bytes")
            print(f"Last modified time: {stat.last_modified}")
            print(f"Permissions: {stat.permissions}")
            print(f"Umask: {stat.umask}")
            print("------")
    except grpc.RpcError as e:
        print(f"RPC failed: {e}")
if __name__ == "__main__":
    target = "{ip}:{port}"  # Replace with your router's IP and gNOI port
    path = "harddisk:"  # Replace with the path you want to check
    username = "{username}"
    password = "{password}"

    perform_stat_operation(target, path, username, password)
