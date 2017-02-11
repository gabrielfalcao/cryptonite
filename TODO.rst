1. Get rid of gnupg2 UI by moving to gnupgme:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Deprecate the ``gnupg`` or ``gnupg2`` binaries in favor of a lib-only interface
- Ensure that no GUI pops up in the following command-line actions:
- Decryption
- Signing
- Generate-key
- Import keys from:
  - designed servers (pgp.mit.edu, etc) (default)
  - HTTP URL, e.g: https://keybase.io/d4v1ncy/key.asc (fallback #1)
  - local file, e.g: mary-mctest.pub

**Relevant links:**

- https://www.hackdiary.com/2004/01/18/revoking-a-gpg-key/
- http://pygpgme.readthedocs.io/en/latest/
- https://github.com/rshk/pygpgme

2. Support for key trust:
~~~~~~~~~~~~~~~~~~~~~~~~~

- Add feature to sign and verify the TRUST\_LEVEL of any keys
- Add feature to send and retrieve keys from all major keyservers:
- http://pgp.mit.edu/
- http://zimmermann.mayfirst.org/
- http://subkeys.pgp.net:11371/
- http://keyserver.ubuntu.com/
- http://sks.spodhuis.org/
- https://sks-keyservers.net/i/
- https://keyserver.pgp.com/
- https://pgp.key-server.io/


3. Implement key vault backed by symmetric encryption:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Implement support for the ciphers + operation modes:
  - AES-CBC (128 or 256 bits for small and medium files)
  - AES-CTR (128 or 256 for all file sizes + generic stream API)

- Support *multi-layered encription* with:
  - AES-CBC (128 and 256)
  - AES-CTR (128 and 256)
  - Password-protected zip blob of the serialized ``Node``

- Research how to implement multi-factor auth in desktop applications
- Research the possibility of using multi-factor auth to compose the AES key.
- Can it be used to derive the IV?
- Can it be used in the PBKDF2-HMAC process?
- Consider using the `HDF5 format <https://support.hdfgroup.org/HDF5/>`_ for storage

**Relevant links:**

- https://www.owasp.org/index.php/Password\_Storage\_Cheat\_Sheet
- https://www.nccgroup.trust/us/about-us/newsroom-and-events/blog/2015/march/enough-with-the-salts-updates-on-secure-password-schemes/
- http://www.daemonology.net/blog/2009-06-11-cryptographic-right-answers.html
- https://www.dlitz.net/software/pycrypto/api/2.6/
- http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/
- http://www.mindrot.org/projects/py-bcrypt/

4. Increase security
~~~~~~~~~~~~~~~~~~~~

- rename process with *setproctitle* to redact secrets
- cleanup environment variables after reading configuration
- scrub bytes of all used files:
  1. write random bytes
  2. fsync
  3. write null bytes
  4. fsync
  5. go back to **#1** X amount of times
- option to use another system user to own the physical file
- set permissions 0400 in every file, only set to 0600 when need to write
- consider sandboxing: https://pypi.python.org/pypi/pysandbox/

**Relevant links:**

- https://pypi.python.org/pypi/setproctitle

5. Implement password management that is more secure than KeepAssX
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1. Use a tree-based data-storage
2. Support multi-factor authentication:

- Master password +
   `TOTP <https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm>`__
   (leverage Google Authenticator/Authy)
- Master password +
   `YubiKey <https://github.com/Yubico/python-yubico>`__
- Master password + binary key file (as in KeepAssX)
- Master password only (warn about lack of OPSec)

3. Support a single master password
4. Support master password **Nomenclature:**
5. Password generation:
  - collect entropy from mouse + keyboard (ala KeePassX)
    - http://www.bitbabbler.org/how.html
    - http://cromwell-intl.com/linux/dev-random.html
    - https://www.blackhat.com/docs/us-15/materials/us-15-Potter-Understanding-And-Managing-Entropy-Usage-wp.pdf
    - http://stackoverflow.com/questions/15129304/best-python-way-to-harvest-user-entropy-from-keystrokes-a-la-pgp
  - https://github.com/drduh/macOS-Security-and-Privacy-Guide?utm_campaign=explore-email&utm_medium=email&utm_source=newsletter&utm_term=daily#passwords


6. _(consideration)_ Generate one-time-passwords that can be used as ``CRYPTONITE_OTP_TOKEN`` environment variable to unlock the vault.

7. Support clipboard: https://github.com/terryyin/clipboard


Reference links
...............

- https://tonyarcieri.com/4-fatal-flaws-in-deterministic-password-managers

+-----------------------------------+-----------------------------------------+
| Component name                    | Description                             |
+===================================+=========================================+
| ``cryptonite.vault.models.Node``  | base-class for all secrets that packs   |
|                                   | the following common features:          |
|                                   | - password protection with through:     |
|                                   |   - AES-128-CTR                         |
|                                   |   - AES-256-CTR                         |
|                                   |   - AES-256-CBC                         |
|                                   |   - AES-256-CBC                         |
|                                   | - serialization                         |
|                                   | and the following common fields:        |
|                                   | - Label                                 |
|                                   | - Description                           |
|                                   | - indexed (bool) - whether to show in   |
|                                   |   the list, auto-complete etc           |
+-----------------------------------+-----------------------------------------+
| ``cryptonite.vault.Item``         | a ``Node`` that contains a single       |
|                                   | secret entry with the limited fields:   |
|                                   | - Username                              |
|                                   | - Password                              |
|                                   | - Email                                 |
|                                   | - Binary Attachment                     |
|                                   | - Comments                              |
+-----------------------------------+-----------------------------------------+
| ``cryptonite.vault.Login``        | a ``Node`` that contains login-related  |
|                                   | fields:                                 |
|                                   | - Username                              |
|                                   | - Password                              |
|                                   | - Email                                 |
|                                   | - Comments                              |
+-----------------------------------+-----------------------------------------+
| ``cryptonite.vault.BinaryBlob``   | a ``Node`` whose contents are binary    |
|                                   | and can be stored:                      |
|                                   | - in the tree as any other ``Node``     |
|                                   | - in an isolated filesystem location    |
+-----------------------------------+-----------------------------------------+
| ``cryptonite.vault.Group``        | A cluster of ``Node`` objects, which    |
|                                   | includes other nodes                    |
+-----------------------------------+-----------------------------------------+



6. Important details to ensure a slick and attractive command-line experience:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add bash-completion support:
- copy implementation from `sagacity <https://github.com/>`_
- auto-complete actions:

 -  ``$ cryptonite <tab>`` suggests ``list``, ``decrypt``, ``encrypt``,
      ``generate``, ``import`` *etc*.

- auto-complete all optional arguments of each ection:

 -  ``$ cryptonite decrypt <tab>`` suggests ``--secret``, ``--no-secret``
      and ``-n``

- Create homebrew *"package"*

- Auto-install bash-completion:
  -  brew (easy)
  -  pip (research how)

7. Consider renaming the project to something more attractive to crypto-newbies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Some ideas _(all available in pypi)_:**

- ``crypt`` - yes, this is available in pypi
- ``cryptonite`` - yep, also available
- ``scopophobia`` - kinda creepy but somewhat a substantial name
- ``cybertoolbox`` - *(cheesy ?!)*
- ``cybercase`` - as in a tool case *(cheesy ?!)*
- ``cipherpunk``
- ``hexspeak``
- ``colorful`` - as in the youtube explanations about [diffie-hellman](https://www.youtube.com/watch?v=YEBfamv-_do) encryption
- ``hushhush``
- ``hush-hush``
- ``privacy``
- ``privacy-toolkit``
- ``freedom``
- ``freedom-toolkit``
- ``crypto-chick``
- ``human-crypto``
- ``pretty-good``


8. Consider creating features to remove sensitive data from known file types before encrypting them:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Set _"stat"_ dates:
  - st_birthtime
  - st_atime
  - st_mtime
  - st_ctime
- EXIF data from JPEG files
- ID3 from:
  - mpeg
  - mpg
  - mp3
  - mp4
- Video metadata:
  - wmv
  - mkv

9. consider linking to these videos:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- https://www.youtube.com/watch?v=1-MPcUHhXoc
- https://www.youtube.com/watch?v=YEBfamv-_do

10. User-experience features:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- warn users when PGP encrypting to themselves.
- create a new system user with limited restrictions
- create chrome extension:
  - auto login with saved passwords
  - auto-visit encrypted favorites

Notes
~~~~~

- Talk about:
  - https://blog.cryptographyengineering.com/2014/08/13/whats-matter-with-pgp/
  - http://secushare.org/PGP

- Check these links:
  - https://pypi.python.org/pypi/ptyprocess
  - https://bitbucket.org/leapfrogdevelopment/rstr/
  - https://www.crypto101.io/
  - https://en.wikipedia.org/wiki/Public-key_cryptography

- Check these modules:
  - https://pypi.python.org/pypi/regex
  - https://pypi.python.org/pypi/range-regex
  - https://pypi.python.org/pypi/pyregex
  - https://pypi.python.org/pypi/regexdict
  - https://pypi.python.org/pypi/regex2dfa
  - https://pypi.python.org/pypi/regex4dummies


extra considerations
--------------------

Features
~~~~~~~~

- builtin email client that authenticates from `Email` *nodes*
  - connect and list inbox
  - connect and list sent
  - connect and list sent
  - conn
  - sigaint support

Environment Variables
~~~~~~~~~~~~~~~~~~~~~


**study the security implications of:**
- `PYTHONUNBUFFERED <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED>`_
- `PYTHONDONTWRITEBYTECODE <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE>`_
- `PYTHONOPTIMIZE <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE>`_
- `PYTHONDEBUG <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDEBUG>`_
- `PYTHONIOENCODING <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONIOENCODING>`_
- `PYTHONINSPECT <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONINSPECT>`_
- `PYTHONNOUSERSITE <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONNOUSERSITE>`_
- `PYTHONUSERBASE <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUSERBASE>`_
- `PYTHONWARNINGS <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONWARNINGS>`_
- `PYTHONWARNINGS <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONWARNINGS>`_
- `PYTHONFAULTHANDLER <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONFAULTHANDLER>`_
- `PYTHONTRACEMALLOC  <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONFAULTHANDLER>`_
- deny to run if `PYTHONSTARTUP` is set as way to prevent exploitation of user runtime.


**if any of the dangerous environment variables are set in the user's environment:**


when using from command line:
  - warn user about all the cases and why it's dangerous
  - exit with _non-zero_ status

when using as python module:
  - raise exception

- set `PYTHONHASHSEED` after collecting entropy
- set `PYTHONEXECUTABLE` to `cryptonite`

exception handling
~~~~~~~~~~~~~~~~~~

use sys.exc_info() somewhere, it can provide useful metadata


- https://docs.python.org/2.7/library/argparse.html#parser-defaults
- https://pypi.python.org/pypi/steganography/0.1.1
- https://pypi.python.org/pypi/Stegano
- https://github.com/RobinDavid/LSB-Steganography
- https://github.com/cedricbonhomme/Stegano
- http://interactivepython.org/runestone/static/everyday/2013/03/1_steganography.html
- https://en.wikipedia.org/wiki/OpenPuff
- https://en.wikipedia.org/wiki/StegFS
- https://en.wikipedia.org/wiki/StegoShare
- http://resources.infosecinstitute.com/steganography-and-tools-to-perform-steganography/
- https://bitbucket.org/skskeyserver/sks-keyserver/wiki/Home
- https://github.com/henryboldi/felony/releases/tag/0.10.3
- https://github.com/HR/Crypter/releases/tag/v2.0.0

- https://github.com/nusenu/ansible-relayor
- https://github.com/systemli/ansible-role-hidden-service
- http://jordan-wright.com/blog/2014/10/06/creating-tor-hidden-services-with-python/
- https://www.torproject.org/docs/tor-hidden-service.html.en#two
- https://stem.torproject.org/tutorials/over_the_river.html
- https://stem.torproject.org/api/control.html#stem.control.Controller.create_hidden_service
- https://stem.torproject.org/tutorials/mirror_mirror_on_the_wall.html
- https://stem.torproject.org/tutorials/east_of_the_sun.html
- https://stem.torproject.org/tutorials/down_the_rabbit_hole.html
- https://stem.torproject.org/tutorials/double_double_toil_and_trouble.html
- https://stem.torproject.org/api.html
