
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class Signature():
    def _hash(self, data: bytes) -> SHA256.SHA256Hash:
        return SHA256.new(data)

    def create(self, data: bytes) -> tuple[RSA.RsaKey, bytes]:
        hash = self._hash(data)
        rsa_key = RSA.generate(2048)
        public_key = rsa_key.public_key()
        signature = pkcs1_15.new(rsa_key).sign(hash)
        return public_key, signature

    def verify(self, data: bytes, public_key: bytes, signature: bytes) -> bool:
        hash = self._hash(data)
        rsa_key = RSA.import_key(public_key)
        try:
            pkcs1_15.new(rsa_key).verify(hash, signature)
            return True
        except ValueError:
            return False
