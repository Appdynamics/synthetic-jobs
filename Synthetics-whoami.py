import requests
import pysftp
import os 

# settings for retrieving certificate files
cert_host = 'ec2-18-220-163-145.us-east-2.compute.amazonaws.com'
user_name = '<%CharlesLin-AWS-SFTP-User%>'
user_secret = "<%CharlesLin-AWS-SFTP-Secret%>"

# settings for test target
target_url = 'https://ec2-18-220-163-145.us-east-2.compute.amazonaws.com/api/v1.0/whoami'

# show the folder to store the certificate files
print(os.path.dirname(os.path.realpath(__file__)))

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection(cert_host, username=user_name, password=user_secret, cnopts=cnopts) as sftp:
    # Fetch the certificate files
    sftp.get('client.crt') 
    sftp.get('client.key')
    sftp.get('server.crt')

response=requests.get(target_url, cert=('client.crt', 'client.key'), verify='server.crt')
print (response.text)

assert('test-client' in response.text)