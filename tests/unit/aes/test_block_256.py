# -*- coding: utf-8 -*-
from cryptonite.aes.blocks import Block256
from cryptonite.exceptions import AESIVPackingError
from cryptonite.exceptions import AESUnpaddingError


def test_padding_void():
    ('Block256.pad should do nothing if the length of the string is divisible by 32')

    data = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    Block256.pad(data).should.equal(data)


def test_padding_256():
    ('Block256.pad should pad up to 32 different bytes')

    Block256.pad('x').should.equal('x' + '\x1f' * 31)
    Block256.pad('xx').should.equal('xx' + '\x1e' * 30)
    Block256.pad('xxx').should.equal('xxx' + '\x1d' * 29)
    Block256.pad('xxxx').should.equal('xxxx' + '\x1c' * 28)
    Block256.pad('xxxxx').should.equal('xxxxx' + '\x1b' * 27)
    Block256.pad('xxxxxx').should.equal('xxxxxx' + '\x1a' * 26)
    Block256.pad('xxxxxxx').should.equal('xxxxxxx' + '\x19' * 25)
    Block256.pad('xxxxxxxx').should.equal('xxxxxxxx' + '\x18' * 24)
    Block256.pad('xxxxxxxxx').should.equal('xxxxxxxxx' + '\x17' * 23)
    Block256.pad('xxxxxxxxxx').should.equal('xxxxxxxxxx' + '\x16' * 22)
    Block256.pad('xxxxxxxxxxx').should.equal('xxxxxxxxxxx' + '\x15' * 21)
    Block256.pad('xxxxxxxxxxxx').should.equal('xxxxxxxxxxxx' + '\x14' * 20)
    Block256.pad('xxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxx' + '\x13' * 19)
    Block256.pad('xxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxx' + '\x12' * 18)
    Block256.pad('xxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxx' + '\x11' * 17)
    Block256.pad('xxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxx' + '\x10' * 16)
    Block256.pad('xxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxx' + '\x0f' * 15)
    Block256.pad('xxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxx' + '\x0e' * 14)
    Block256.pad('xxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxx' + '\r' * 13)
    Block256.pad('xxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxx' + '\x0c' * 12)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxx' + '\x0b' * 11)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxx' + '\n' * 10)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxx' + '\t' * 9)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxxx' + '\x08' * 8)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxxxx' + '\x07' * 7)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x06' * 6)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x05' * 5)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x04' * 4)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x03' * 3)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x02' * 2)
    Block256.pad('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x01' * 1)


def test_unpadding_256_invalid_offset():
    ('Block256.unpad should raise an exception if the provided string has invalid length')

    Block256.unpad.when.called_with('error').should.have.raised(
        AESUnpaddingError,
        'Block256.unpad() got invalid string with length=5 and offset=27'
    )


def test_unpadding_256():
    ('Block256.unpad should unpad up to 32 different bytes')

    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x01').should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x02' * 2).should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x03' * 3).should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x04' * 4).should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x05' * 5).should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxxxxx' + '\x06' * 6).should.equal('xxxxxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxxxx' + '\x07' * 7).should.equal('xxxxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxxx' + '\x08' * 8).should.equal('xxxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxxx' + '\t' * 9).should.equal('xxxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxxx' + '\n' * 10).should.equal('xxxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxxx' + '\x0b' * 11).should.equal('xxxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxxx' + '\x0c' * 12).should.equal('xxxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxxx' + '\r' * 13).should.equal('xxxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxxx' + '\x0e' * 14).should.equal('xxxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxxx' + '\x0f' * 15).should.equal('xxxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxxx' + '\x10' * 16).should.equal('xxxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxxx' + '\x11' * 17).should.equal('xxxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxxx' + '\x12' * 18).should.equal('xxxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxxx' + '\x13' * 19).should.equal('xxxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxxx' + '\x14' * 20).should.equal('xxxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxxx' + '\x15' * 21).should.equal('xxxxxxxxxxx')
    Block256.unpad('xxxxxxxxxx' + '\x16' * 22).should.equal('xxxxxxxxxx')
    Block256.unpad('xxxxxxxxx' + '\x17' * 23).should.equal('xxxxxxxxx')
    Block256.unpad('xxxxxxxx' + '\x18' * 24).should.equal('xxxxxxxx')
    Block256.unpad('xxxxxxx' + '\x19' * 25).should.equal('xxxxxxx')
    Block256.unpad('xxxxxx' + '\x1a' * 26).should.equal('xxxxxx')
    Block256.unpad('xxxxx' + '\x1b' * 27).should.equal('xxxxx')
    Block256.unpad('xxxx' + '\x1c' * 28).should.equal('xxxx')
    Block256.unpad('xxx' + '\x1d' * 29).should.equal('xxx')
    Block256.unpad('xx' + '\x1e' * 30).should.equal('xx')
    Block256.unpad('x' + '\x1f' * 31).should.equal('x')


def test_pack_iv():
    ('Block256.pack_iv_and_ciphertext() should put the iv in front of the string')

    iv = 'y' * 16
    ciphertext = 'crypt0crypt0crypt0crypt0crypt0crypt0'
    result = Block256.pack_iv_and_ciphertext(iv, ciphertext)

    result.startswith(iv).should.be.true
    result.endswith(ciphertext).should.be.true


def test_pack_iv_wrong_size():
    ('Block256.pack_iv_and_ciphertext() should raise an exception if the iv has a different size than expected')

    iv = 'y' * 32
    when_called = Block256.pack_iv_and_ciphertext.when.called_with(iv, 'foobar')
    when_called.should.have.raised(
        AESIVPackingError,
        'Block256.pack_iv_and_ciphertext() failed because the provided iv has wrong length: 32 != 16',
    )


def test_unpack_iv():
    ('Block256.pack_iv_and_ciphertext() should put the iv in front of the string')

    iv = 'y' * 16
    ciphertext = 'crypt0crypt0crypt0crypt0crypt0crypt0'

    packed = Block256.pack_iv_and_ciphertext(iv, ciphertext)
    result = Block256.unpack_iv_and_ciphertext(packed)

    result[0].should.equal(iv)
    result[1].should.equal(ciphertext)
