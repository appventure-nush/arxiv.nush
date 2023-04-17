from io import BytesIO
import base64

def convertB64toBytes(b64):
    f = BytesIO()
    f.write(base64.b64decode(b64))
    f.seek(0)
    bytes = f.read()
    f.close()
    return bytes

def removeNulls(arr):
    return [i for i in arr if i]