.. _AES Symmetrical Encryption:


AES Modes of Operation
======================

Simple python `DSL <https://en.wikipedia.org/wiki/Domain-specific_language>`_ for AES-based symmetrical encryption of files and strings. Powered by `PyCrypto <>https://www.dlitz.net/software/pycrypto/api/current/`_ and `cryptography <https://cryptography.io/en/latest/>`_


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
