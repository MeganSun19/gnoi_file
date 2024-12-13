# gNOI File Operation(Stat/Remove)

## Overview

Python script uses gNOI File Stat RPC to retrieve metadata about a file or remove a file.

---


## Prerequisites:
	- Install Python and Required Libraries:
      Ensure Python 3.6 or later is installed.
	- Install gRPC ibraries:
     pip install grpcio grpcio-tools protobuf

## Steps

1. **Download the Required `.proto` Files**
   - https://github.com/openconfig/gnoi/blob/main/file/file.proto
2. **Complile the '.proto' files**
   - Use `grpcio-tools` to generate Python gRPC and message classes:
     ```bash
     python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. github.com/openconfig/gnoi/os.proto
     ```
   - Repeat this step for all required `.proto` files.


3. **Set Up Credentials (Optional, if using secure gRPC)**
	- Obtain the root CA certificate for the device and save it (e.g., 'CA.cer').
    - Update the 'cert_cn' and the and certificate paths in the script as needed.


