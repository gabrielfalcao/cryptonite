BLKSIZE = 16
x = []
for plainsize in range(1, BLKSIZE):
    padsize = BLKSIZE - plainsize
    string = 'x' * plainsize
    x.append("    Block128.pad('{0}').should.equal({1} * {2})".format(string, repr(string) + ' + ' + repr(chr(padsize)), padsize))

with open('clipboard.txt', 'w')as fd:
    fd.write('\n'.join(x))
