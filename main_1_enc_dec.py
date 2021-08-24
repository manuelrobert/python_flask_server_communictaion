from flask import Flask
from flask_cors import CORS
import requests, rsa

app = Flask(__name__)
CORS(app)

api = 'http://localhost:3000/getdata'
headers = {'content-type': 'application/json'}

def createPublicAndPrivateKeys():
    publicKey, privateKey = rsa.newkeys(2048) 
    publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8') 
    with open('public.pem','w+') as f: f.write(publicKeyPkcs1PEM)
    privateKeyPkcs1PEM = privateKey.save_pkcs1().decode('utf8') 
    with open('private.pem','w+') as f: f.write(privateKeyPkcs1PEM)

def readPublicKey():
    with open('public.pem', mode='rb') as f: return rsa.PublicKey.load_pkcs1(f.read())

def readPrivateKey():
    with open('private.pem', mode='rb') as f: return rsa.PrivateKey.load_pkcs1(f.read())


createPublicAndPrivateKeys()

@app.route('/senddata', methods = ['GET','POST'])
def send_data():
    print('***********************IN SEND_DATA*******************')

    data = 'sample data'
    print('data', data)

    plaintext = data.encode('utf8')
    print('plaintext', plaintext)

    ciphertext = rsa.encrypt(plaintext, readPublicKey())
    print('ciphertext', ciphertext)

    body = {'data': ciphertext.hex()}
    print(body)

    res = requests.post(url = api , json=body, headers = headers)
    print('result', res.json())
    
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=4000)