Cryptonite - Cryptography for Humans
====================================

- Sandboxed GPG keyrings
- AES Encryption
  - 128-CBC
  - 128-CTR
  - 256-CBC
  - 256-CTR


Quick Start
###########

.. code:: bash

   $ pip install cryptonite

GPG
~~~


Create a new GPG keyring
------------------------

.. code:: python

   from cryptonite.gpg import GPGKeyring


   sandbox = GPGKeyring(path='/srv/data/gpg-keyrings/genkey-example')

   fingerprint = sandbox.generate_key(
       'Full User Name',
       'some@email.com',
       block_size=4096,
       passphrase_callback='123456',
   )

   # Encrypting data
   ciphertext = sandbox.encrypt('sensitive plain-text', fingerprint)

   # Decrypting data
   plaintext = sandbox.decrypt(ciphertext, passphrase_callback=lambda: "123456")

   assert plaintext == 'sensitive plain-text'


Get the private key
------------------

.. code:: python

   from cryptonite.gpg import GPGKeyring

   keyring = GPGKeyring(
       path='/srv/data/gpg-keyrings/get-private',
   )
   fingerprint = sandbox.generate_key(
       'Full User Name',
       'some@email.com',
       block_size=4096,
       passphrase_callback=lambda: "123456"
   )

   private_key = keyring.get_private_key(fingerprint)
   assert 'PRIVATE' in private


Get the public key
------------------

.. code:: python

   from cryptonite.gpg import GPGKeyring

   keyring = GPGKeyring(
       path='/srv/data/gpg-keyrings/get-public',
   )
   fingerprint = sandbox.generate_key(
       'Full User Name',
       'some@email.com',
       block_size=4096,
       passphrase_callback=lambda: "123456"
   )

   public_key = keyring.get_public_key(fingerprint)
   assert 'PUBLIC' in public


Import a key from a file
------------------------

.. code:: python

   from cryptonite.gpg import GPGKeyring

   sources = GPGKeyring(
       path='/srv/data/gpg-keyrings/genkey-stub1',
   )
   source_fingerprint = sandbox.generate_key(
       'Full User Name',
       'some@email.com',
       block_size=4096,
       passphrase=None
   )
   with open('/tmp/private.key', 'wb') as fp:
       fp.write(sandbox.get_private_key(source_fingerprint))

   sandbox = GPGKeyring(
       path='/srv/data/gpg-keyrings/import-from-web',
   )

   fingerprint = sandbox.import_from_path(
       'tmp/private.key'
   )

   assert fingerprint == source_fingerprint


Import a key from known servers
-------------------------------

.. code:: python

   from cryptonite.gpg import GPGKeyring


   sandbox = GPGKeyring(
       path='/srv/data/gpg-keyrings/import-from-web',
       keyservers=[
           'certserver.pgp.com',
           'pgp.cs.uu.nl',
           'pgp.mit.edu',
           'sks-keyservers.net',
       ]
   )

   fingerprint = sandbox.import_from_web(
       'abaf11c65a2970b130abe3c479be3e4300411886'
   )

   assert fingerprint == 'abaf11c65a2970b130abe3c479be3e4300411886'


AES
===

AES CBC 128 and 256 bits
------------------------

.. code:: python

   from cryptonite.aes.cbc import AES128CBC
   # or
   # from cryptonite.aes.cbc import AES256CBC

   cbc128 = AES128CBC()

   ciphertext = cbc128.encrypt('sensitive plain-text', 's3cre7p4ssw0rd')
   plaintext = cbc128.decrypt(ciphertext, 's3cre7p4ssw0rd')
   assert plaintext == 'sensitive plain-text'


AES CTR 128 and 256 bits
------------------------

.. code:: python

   from cryptonite.aes.ctr import AES128CTR
   # or
   # from cryptonite.aes.ctr import AES256CTR

   ctr128 = AES128CTR()

   ciphertext = ctr128.encrypt('sensitive plain-text', 's3cre7p4ssw0rd')
   plaintext = ctr128.decrypt(ciphertext, 's3cre7p4ssw0rd')
   assert plaintext == 'sensitive plain-text'
