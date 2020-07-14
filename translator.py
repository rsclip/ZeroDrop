import math
from Crypto.Cipher import AES
from binascii import unhexlify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import random
import re


class Translator:
    def __init__(self):
        self.SymmetricalEncryption = SymmetricalEncryption()
        self.AsymmetricEncryption = AsymmetricEncryption()
        self.Conversion = Conversion()

    def slice(self, public, private, n, options):
        '''
        Slice public message in chunks of n (220)
        Slice private key in proportionally similar
         sizes.
        Amount of public key chunks = Amount of
         private key chunks
        '''
        if 'noslice' in options:
            public, private = [public], [private]
        elif len(public) > n:
            m = math.floor(220/len(public) * len(private))
            public = [public[i:i+n] for i in range(0, len(public.strip('\r').strip('\n')), n)]
            private = [private[i:i+n] for i in range(0, len(private.strip('\r').strip('\n')), m)]
        else:
            public, private = [public], [private]
        return public, private

    def getMapping(self, public, private):
        '''
        Returns [[public, private], [public, private]]
        Essentially a sorted dictionary
        '''
        map = []
        for i, j in enumerate(public):
            map.append([j, private[i]])
        return map

    def verifyPGP(self, pgpKey):
        if pgpKey.startswith('-----BEGIN PUBLIC KEY-----') and pgpKey.endswith('-----END PUBLIC KEY-----\n') and len(pgpKey) > 100:
            # Probably correct, to catch common errors
            return True
        elif pgpKey.startswith('-----BEGIN PRIVATE KEY-----') and pgpKey.endswith('-----END PRIVATE KEY-----\n') and len(pgpKey) > 1000:
            # Probably correct, to catch common errors
            return True
        else:
            return False

    def insertMessage(self, public, private):
        public = public.split()
        wordIndex = random.randint(1, len(public)-1)
        public[wordIndex] = private + public[wordIndex]
        return ' '.join(public)

    def findContent(self, text):
        result = re.search('\u200e(.*)\u200e', text)
        private = result.group(1)
        public = text.replace('\u200e', '').replace(private, '')
        return public, private


class Conversion:
    def __init__(self):
        self.charset = ['\u200b', '\u200c', '\u200d']
        self.startStop = '\u200e'

    def _toBinary(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def _toText(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

    def convertTextBinary(self, text):
        text = text.split(' ')
        text = [str(self._toBinary(i)) for i in text]
        return int('2'.join(text))

    def convertBinaryText(self, binary):
        binary = str(binary).split('2')
        binary = [self._toText(i) for i in binary]
        return ' '.join(binary)

    def convertBinaryZero(self, binary):
        return self.startStop + str(binary).replace('0', self.charset[0]).replace('1', self.charset[1]).replace('2', self.charset[2]) + self.startStop

    def convertZeroBinary(self, zero):
        '''
        Must find the 2 self.startStop variables, remove and
        pass the zero argument as the content between them.
        '''
        return int(str(zero).replace(self.charset[0], '0').replace(self.charset[1], '1').replace(self.charset[2], '2'))


class AsymmetricEncryption:
    def __init__(self):
        pass

    def loadPrivate(self, text):
        return serialization.load_pem_private_key(
            text.encode(),
            password=None,
            backend=default_backend()
        )

    def loadPublic(self, text):
        return serialization.load_pem_public_key(
            text.encode(),
            backend=default_backend()
        )

    def encrypt(self, message, public_key):
        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted.hex()

    def decrypt(self, message, private_key):
        original_message = private_key.decrypt(
            unhexlify(message),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return original_message.decode()


class SymmetricalEncryption:
    def __init__(self):
        pass

    def encrypt(self, message, key, iv):
        obj = AES.new(key.encode(), AES.MODE_CFB, iv.encode())
        return obj.encrypt(message.encode()).hex()

    def decrypt(self, message, key, iv):
        obj2 = AES.new(key.encode(), AES.MODE_CFB, iv.encode())
        return obj2.decrypt(unhexlify(message.encode())).decode('utf8')
