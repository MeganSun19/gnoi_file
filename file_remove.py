import grpc
from github.com.openconfig.gnoi.file import file_pb2, file_pb2_grpc
from github.com.openconfig.gnoi.common import common_pb2
from github.com.openconfig.gnoi.types import types_pb2
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
def perform_stat_operation(stub, path):
    # Create Stat request
    request = file_pb2.StatRequest(path=path)

    try:
        # Perform Stat RPC call
        response = stub.Stat(request)
        print(f"Stat response for {path}: {response}")
        return True
    except grpc.RpcError as e:
        print(f"Stat RPC failed: {e}")
        return False

def perform_remove_operation(target, path, username, password):
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
    channel = grpc.secure_channel(target, composite_creds, options)

    # Create gNOI File service stub
    stub = file_pb2_grpc.FileStub(channel)
 
    # Verify file existence using Stat request
    if not perform_stat_operation(stub, remote_file_path):
        print(f"File {remote_file_path} does not exist or cannot be accessed.")
        return

    try:
        # Create RemoveRequest with the correct field
        request = file_pb2.RemoveRequest(remote_file=remote_file_path)
    except ValueError as e:
        print(f"Failed to create RemoveRequest: {e}")
        return

    # Debug information
    print(f"Attempting to remove file: {remote_file_path}")

    try:
        # Perform Remove RPC call
        response = stub.Remove(request)
        print(f"Remove successful for {remote_file_path}: {response}")
    except grpc.RpcError as e:
        print(f"RPC failed: {e}")
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print("Error: The specified file was not found.")
        elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
            print("Error: Permission denied.")
        elif e.code() == grpc.StatusCode.INTERNAL:
            print("Error: Internal error occurred.")
        else:
            print(f"Error code: {e.code()}, details: {e.details()}")


if __name__ == "__main__":
    target = "{ip}:{port}"  # Replace with your router's IP and gNOI port
    remote_file_path = "harddisk:/test.txt"  # Replace with the specific file path you want to remove
    username = "{username}"
    password = "{password}"

    perform_remove_operation(target, remote_file_path, username, password)