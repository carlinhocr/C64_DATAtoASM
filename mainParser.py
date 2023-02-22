class DataParser(object):

    def __init__(self):
        pass

    def codeDecimalTOhex(self,instructionDecimal):
        return hex(int(instructionDecimal))[2:].upper() #[2:] to strip the 0x from the string
        pass

    def instructionFull(self,instructionHex):
        #inmediate expects a literal (1 byte). LDA #$FF
        #zeropage expects a byte (1 byte) with a position of memory on the zero page 00XX. LDA $2
        #implied expects no arguments (0 bytes). CLI
        #indirect indexed. LDA($FD),Y
        instruction = {
            # number of bytes that follow, mnemonic, memory addressing mode, hex code
            "9": [1, "ORA", "inmediate", "9"],
            "29": [1, "AND", "inmediate", "29"],
            "58": [0, "CLI", "implied", "58"],
            "60": [0, "RTS", "implied", "60"],
            "78": [0, "SEI", "implied", "78"],
            "85": [1, "STA", "zeropage", "85"],
            "A0": [1, "LDY", "inmediate", "A0"],
            "A5": [1, "LDA", "zeropage", "A5"],
            "B1": [1, "LDA", "indirectindexed", "B1"],
                       }
        if instructionHex.upper() in instruction.keys():
            return instruction[instructionHex.upper()]
        else:
            print("bad parsing instruction for 6502 not found")
            exit(-2)

    def fromDecimalString_toHexCode(self,codeString):
        #get a list of strings with instructions and bytes
        byteList = self.prepareCodeForParsing(codeString)
        print("byte list",byteList)
        #parse to a list of isntruction code and paramenters as a sublist according to its memory addresing
        instructionHexaParsedList = []
        byteListPosition = 0
        end = len(byteList)
        while byteListPosition < end:
            byte = byteList[byteListPosition]
            hexInstruction = self.codeDecimalTOhex(byte)
            instructionFullElement = self.instructionFull(hexInstruction)
            arguments = instructionFullElement[0]
            print(instructionFullElement,arguments)
            instructionlist=[]
            if arguments == 0:
                instructionlist.append(hexInstruction)
                byteListPosition += 1
            else:
                for i in (0,arguments):
                    hexElement = self.codeDecimalTOhex(byteList[byteListPosition])
                    print (hexElement)
                    instructionlist.append(hexElement)
                    byteListPosition += 1
            instructionHexaParsedList.append(instructionlist)
            print ("byteListPosition", byteListPosition)
            print (instructionHexaParsedList)
        #return list of strings with sublists of instructions and parameters
        return instructionHexaParsedList

    def fromHexCode_tomnemonicCode(self,instructionHexaParsedList):
        #get a list of strings with sublists of instructions and parameters
        for instructionLine in instructionHexaParsedList:
            print(self.instructionFull(instructionLine[0])[1])
        #proper format it as mnemonics and $ and # formatting
        pass

    def prepareCodeForParsing(self,codeString):
        # strip the 10 DATA
        upperString = codeString.upper()
        position = upperString.find("DATA")
        noDataString = upperString[position+4:]
        cleanString = noDataString.replace(" ","")
        if self.checkCommaAndDigitsOnly(cleanString):
            print("the string is not formatted as only line number, data,and comma separated numbers")
            exit(-1)
        # parse the comma separated string and add to a list of strings
        byteList = cleanString.split(",")
        #return the list of strings
        return byteList

    def checkCommaAndDigitsOnly(self,checkString):
        badString = False
        for letter in checkString:
            if letter.isnumeric() is True or letter == ",":
                pass
            else:
                badString = True
        return badString

def main():
    dp = DataParser()
    instructionLine ="10 data 120, 165, 1, 41, 252, 133, 1, 160, 0, 177, 251, 133,2, 165, 1, 9, 3, 133, 1, 88, 96"
    instructionsInHexa = dp.fromDecimalString_toHexCode(instructionLine)
    dp.fromHexCode_tomnemonicCode(instructionsInHexa)
    # instructionDecimal = "165"
    # instructionHex = dp.codeDecimalTOhex(instructionDecimal)
    # instructionFull = dp.instructionTobytes(instructionHex)
    #print(instructionFull)

if __name__ == "__main__":
    main()