import hashlib

class RanCode:
    def __init__(self, seed):
        self.phonemes = ['a', 'e', 'i', 'o', 'u', 'k', 'l', 'm', 'n', 'p', 's', 't', 'w', 'j', 'd', 'x']
        self.phonemes.sort()
        self.key = seed

    def rehash(self):
        digest = hashlib.sha3_512(self.key.encode()).hexdigest()
        self.key = digest

    def createKnuthIndex(self, hex):
        index = []
        for i in range(16):
            num = int(hex[i*8:(i+1)*8], 16)
            index.append(int(num / 4294967295.0 * (16-i)))
        return index

    def knuthShuffle(self, hex):
        index = self.createKnuthIndex(hex)
        shuffled = self.phonemes.copy()
        for i in range(16):
            dummy = shuffled[i]
            shuffled[i] = shuffled[i+index[i]]
            shuffled[i+index[i]] = dummy
        return shuffled

    def lutEncode(self, inputData, lutData):
        index = self.phonemes.index(inputData)
        return lutData[index]

    def lutDecode(self, inputData, lutData):
        index = lutData.index(inputData)
        return self.phonemes[index]

    def encode(self, inputData):
        output = ""
        for c in inputData:
            lutData = self.knuthShuffle(self.key)
            output = output + self.lutEncode(c, lutData)
            self.rehash()
        return output

    def decode(self, inputData):
        output = ""
        for c in inputData:
            lutData = self.knuthShuffle(self.key)
            output = output + self.lutDecode(c, lutData)
            self.rehash()
        return output

