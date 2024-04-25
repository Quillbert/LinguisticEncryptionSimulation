import json
import textwrap

class Command:
    markedPhoneme = 'd'
    commandLength = 4

    def __init__(self, comm, encoded=False):
        self.chars = ["a", "e", "i", "j", "k", "l", "m", "n", "o", "p", "s", "t", "u", "w"]
        with open('tokiToEngl.json') as json_file:
            self.tokiToEngl = json.load(json_file)

        with open('englToToki.json') as json_file:
            self.englToToki = json.load(json_file)

        with open('tokiPonaToTwoCharacters.json') as json_file:
            self.mappings = json.load(json_file)

        with open('twoCharactersToTokiPona.json') as json_file:
            self.reverse_mappings = json.load(json_file)

        if(encoded):
            self.command = self.unpadLength(comm)
            self.command = self.fromTwoCharacters(self.command)
            self.command = self.fromTokiPona(self.command)
            
        else:
            self.command = comm

    def getTokiPona(self):
        return self.toTokiPona(self.command)

    def getPadded(self):
        return self.padLength(self.command)
    
    def getOriginal(self):
        return self.command
    
    def toTokiPona(self, comm):
        return self.englToToki[comm]
    
    def fromTokiPona(self, comm):
        parts = comm.split()
        if parts[len(parts)-1][0].isdigit():
            comm = " ".join(parts[0:len(parts)-1])
        toki = self.tokiToEngl[comm]
        if parts[len(parts)-1][0].isdigit():
            toki += " " + parts[len(parts) - 1]
        return toki
    
    def padLength(self, comm):
        parts = comm.split()
        if len(parts) > 1:
            comm = parts[0]
        toki = self.englToToki[comm]
        if len(parts) > 1:
            toki += " " + parts[1]
        twoChars = self.toTwoCharacters(toki)
        noSpace = twoChars.replace(' ', self.markedPhoneme)
        while(len(noSpace)<self.commandLength):
            noSpace = noSpace + self.markedPhoneme
        return noSpace

    def unpadLength(self, comm):
        reg = comm.replace(self.markedPhoneme, ' ')
        return reg.strip()

    def toTwoCharacters(self, comm):
        words = comm.split()
        out = ""
        for word in words:
            if word[0].isdigit():
                out += self.numberToChars(word)
            else:
                out += self.mappings[word]
        return out

    def fromTwoCharacters(self, comm):
        words = textwrap.wrap(comm.strip(), 2)
        temp = []
        prev = ""
        for word in words:
            if prev == "sinpin" or prev == "monsi":
                temp.append(self.charsToNumbers(word))
                prev = ""
            else:
                temp.append(self.reverse_mappings[word])
                prev = self.reverse_mappings[word]
        out = " ".join(temp)
        return out

    def numberToChars(self, num):
        out = ""
        for c in num:
            out += self.chars[int(c)]
        return out

    def charsToNumbers(self, ch):
        out = ""
        for c in ch:
            out += str(self.chars.index(c))
        return out



    
