from flask import Flask, request
from flask_cors import CORS
import requests, rsa


app = Flask(__name__)
CORS(app)

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


@app.route('/getdata', methods = ['GET','POST'])
def get_data():
    print('*********************IN GET_DATA*********************')
    
    print('result', request.get_json())
    
    ciphertext = bytes.fromhex(request.get_json()['data'])
    print('ciphertext', ciphertext)

    decryptedMessage = rsa.decrypt(ciphertext, readPrivateKey()).decode('utf-8')
    print('decryptedMessage', decryptedMessage)

    return {'msg':'ok'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)