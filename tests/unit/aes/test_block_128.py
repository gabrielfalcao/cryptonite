# -*- coding: utf-8 -*-
from cryptonite.aes.blocks import Block128


def test_padding_void():
    ('Block128.pad should do nothing if the length of the string is divisible by 16')

    data = 'xxxxxxxxxxxxxxxx'
    Block128.pad(data).should.equal(data)


def test_padding_128():
    ('Block128.pad should pad up to 16 different bytes')

    Block128.pad('x').should.equal('x' + '\x0f' * 15)
    Block128.pad('xx').should.equal('xx' + '\x0e' * 14)
    Block128.pad('xxx').should.equal('xxx' + '\r' * 13)
    Block128.pad('xxxx').should.equal('xxxx' + '\x0c' * 12)
    Block128.pad('xxxxx').should.equal('xxxxx' + '\x0b' * 11)
    Block128.pad('xxxxxx').should.equal('xxxxxx' + '\n' * 10)
    Block128.pad('xxxxxxx').should.equal('xxxxxxx' + '\t' * 9)
    Block128.pad('xxxxxxxx').should.equal('xxxxxxxx' + '\x08' * 8)
    Block128.pad('xxxxxxxxx').should.equal('xxxxxxxxx' + '\x07' * 7)
    Block128.pad('xxxxxxxxxx').should.equal('xxxxxxxxxx' + '\x06' * 6)
    Block128.pad('xxxxxxxxxxx').should.equal('xxxxxxxxxxx' + '\x05' * 5)
    Block128.pad('xxxxxxxxxxxx').should.equal('xxxxxxxxxxxx' + '\x04' * 4)
    Block128.pad('xxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxx' + '\x03' * 3)
    Block128.pad('xxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxx' + '\x02' * 2)
    Block128.pad('xxxxxxxxxxxxxxx').should.equal('xxxxxxxxxxxxxxx' + '\x01' * 1)


def test_unpadding_128():
    ('Block128.unpad should pad up to 16 different bytes')
    Block128.unpad('xxxxxxxxxxxxxxx' + '\x01' * 1).should.equal('xxxxxxxxxxxxxxx')
    Block128.unpad('xxxxxxxxxxxxxx' + '\x02' * 2).should.equal('xxxxxxxxxxxxxx')
    Block128.unpad('xxxxxxxxxxxxx' + '\x03' * 3).should.equal('xxxxxxxxxxxxx')
    Block128.unpad('xxxxxxxxxxxx' + '\x04' * 4).should.equal('xxxxxxxxxxxx')
    Block128.unpad('xxxxxxxxxxx' + '\x05' * 5).should.equal('xxxxxxxxxxx')
    Block128.unpad('xxxxxxxxxx' + '\x06' * 6).should.equal('xxxxxxxxxx')
    Block128.unpad('xxxxxxxxx' + '\x07' * 7).should.equal('xxxxxxxxx')
    Block128.unpad('xxxxxxxx' + '\x08' * 8).should.equal('xxxxxxxx')
    Block128.unpad('xxxxxxx' + '\t' * 9).should.equal('xxxxxxx')
    Block128.unpad('xxxxxx' + '\n' * 10).should.equal('xxxxxx')
    Block128.unpad('xxxxx' + '\x0b' * 11).should.equal('xxxxx')
    Block128.unpad('xxxx' + '\x0c' * 12).should.equal('xxxx')
    Block128.unpad('xxx' + '\r' * 13).should.equal('xxx')
    Block128.unpad('xx' + '\x0e' * 14).should.equal('xx')
    Block128.unpad('x' + '\x0f' * 15).should.equal('x')
