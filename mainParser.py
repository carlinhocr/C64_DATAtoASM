import sys

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
            "69": [1, "ADC", "immediate", "69","Add memory to accumulator with carry"],
            "65": [1, "ADC", "zeropage", "65", "Add memory to accumulator with carry"],
            "75": [1, "ADC", "zeropagex", "75", "Add memory to accumulator with carry"],
            "6D": [2, "ADC", "absolute", "6D", "Add memory to accumulator with carry"],
            "7D": [2, "ADC", "absolutex", "7D", "Add memory to accumulator with carry"],
            "79": [2, "ADC", "absolutey", "79", "Add memory to accumulator with carry"],
            "61": [1, "ADC", "indexedinderectx", "61", "Add memory to accumulator with carry"],
            "71": [1, "ADC", "indirectindexedy", "71", "Add memory to accumulator with carry"],

            "29": [1, "AND", "immediate", "29", "AND memory with accumulator"],
            "25": [1, "AND", "zeropage", "25", "AND memory with accumulator"],
            "35": [1, "AND", "zeropagex", "35", "AND memory with accumulator"],
            "2D": [2, "AND", "absolute", "2D", "AND memory with accumulator"],
            "3D": [2, "AND", "absolutex", "3D", "AND memory with accumulator"],
            "39": [2, "AND", "absolutey", "39", "AND memory with accumulator"],
            "21": [1, "AND", "indexedinderectx", "21", "AND memory with accumulator"],
            "31": [1, "AND", "indirectindexedy", "31", "AND memory with accumulator"],

            "0A": [0, "ASL", "accumulator", "0A", "Shift left one bit (Memory or Accumulator)"],
            "06": [1, "ASL", "zeropage", "06", "Shift left one bit (Memory or Accumulator)"],
            "16": [1, "ASL", "zeropagex", "16", "Shift left one bit (Memory or Accumulator)"],
            "0E": [2, "ASL", "absolute", "0E", "Shift left one bit (Memory or Accumulator)"],
            "1E": [2, "ASL", "absolutex", "1E", "Shift left one bit (Memory or Accumulator)"],

            "58": [0, "CLI", "implied", "58"],
            "60": [0, "RTS", "implied", "60"],
            "78": [0, "SEI", "implied", "78"],
            "85": [1, "STA", "zeropage", "85"],
            "91": [1, "STA", "indirectindexedy", "91"],
            "A0": [1, "LDY", "inmediate", "A0"],
            "A5": [1, "LDA", "zeropage", "A5"],
            "B1": [1, "LDA", "indirectindexedy", "B1"],
            "9": [1, "ORA", "immediate", "9"],
                       }
        if instructionHex.upper() in instruction.keys():
            return instruction[instructionHex.upper()]
        else:
            print("bad parsing instruction for 6502 not found")
            exit(-2)

    def fromDecimalString_toHexCode(self,codeString):
        #get a list of strings with instructions and bytes
        byteList = self.prepareCodeForParsing(codeString)
        #parse to a list of isntruction code and paramenters as a sublist according to its memory addresing
        instructionHexaParsedList = []
        byteListPosition = 0
        end = len(byteList)
        while byteListPosition < end:
            byte = byteList[byteListPosition]
            hexInstruction = self.codeDecimalTOhex(byte)
            instructionFullElement = self.instructionFull(hexInstruction)
            arguments = instructionFullElement[0]
            instructionlist=[]
            if arguments == 0:
                instructionlist.append(hexInstruction)
                byteListPosition += 1
            else:
                for i in (0,arguments):
                    hexElement = self.codeDecimalTOhex(byteList[byteListPosition])
                    # print (hexElement)
                    instructionlist.append(hexElement)
                    byteListPosition += 1
            instructionHexaParsedList.append(instructionlist)
        #return list of strings with sublists of instructions and parameters
        return instructionHexaParsedList


    def fromHexCode_tomnemonicCode(self,instructionHexaParsedList):
        #get a list of strings with sublists of instructions and parameters
        #proper format it as mnemonics and $ and # formatting
        instructionsMnemonic=[]
        for instructionLine in instructionHexaParsedList:
            fullIntructionInfo = self.instructionFull(instructionLine[0])
            memAddresing = fullIntructionInfo[2]
            stringLine = "\t"
            if memAddresing == "implied":
                stringLine += fullIntructionInfo[1]
            elif memAddresing == "accumulator":
                stringLine += fullIntructionInfo[1]
            elif memAddresing == "absolut":
                stringLine += fullIntructionInfo[1]+" "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine += "$"+element
            elif memAddresing == "absolutx":
                stringLine += fullIntructionInfo[1] + " "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine += "$" + element + ",X"
            elif memAddresing == "absoluty":
                stringLine += fullIntructionInfo[1] + " "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine += "$" + element + ",Y"
            elif memAddresing == "indirectindexedy":
                stringLine += fullIntructionInfo[1]+" "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine += "($"+element+"),Y"
            elif memAddresing == "indexedinderectx":
                stringLine += fullIntructionInfo[1]+" "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine += "($"+element+",X)"
            elif memAddresing == "zeropage":
                stringLine += fullIntructionInfo[1]+" "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine += "$"+element
            elif memAddresing == "zeropagex":
                stringLine += fullIntructionInfo[1]+" "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine += "$"+element+",X"
            elif memAddresing == "immediate":
                stringLine += fullIntructionInfo[1]+" "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine += "#$"+element
            else:
                stringLine += fullIntructionInfo[1]+" "
                # proper format it as mnemonics and $ and # formatting
                element = instructionLine.pop()
                stringLine +=element
            instructionsMnemonic.append(stringLine)
        return instructionsMnemonic

    def prepareCodeForParsing(self,codeString):
        # strip the 10 DATA
        upperString = codeString.upper()
        position = upperString.find("DATA")
        noDataString = upperString[position+4:]
        cleanString = noDataString.replace(" ","")
        if self.checkCommaAndDigitsOnly(cleanString):
            #print("the string is not formatted as only line number, data,and comma separated numbers")
            byteList = []
        else:
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

    def buildBinaryCode(self,hexaStringLines):
        byteString = ""
        for line in hexaStringLines:
            for instruction in line:
                for element in instruction:
                    if len(element) == 1:
                        byteString += "0" + element
                    elif len(element) == 2:
                        byteString += element
                    elif len(element) == 3:
                        lowByte = element[1:]
                        highByte = "0" + element[:1]
                        element = lowByte + highByte
                        byteString += element
                    elif len(element) == 4:
                        lowByte = element[:1]
                        highByte = element[1:]
                        element = lowByte + highByte
                        byteString += element
                    else:
                        print("error in hexa element", element)
                        exit(-3)
        return byteString


    def read_file(self,filename):
        with open(filename,'r') as fileDataBasic:
            dataLines = fileDataBasic.read().strip().splitlines()
        return dataLines

    def write_fileMnemonics(self,filename,instructionMnemonicsLines):
        with open(filename, 'w') as fileMnemonics:
            for line in instructionMnemonicsLines:
                for instruction in line:
                    fileMnemonics.write(instruction+"\n")

    def parseDataFile(self,readFilename,writeFilename):
        dataLines = self.read_file(readFilename)
        hexaStringLines = []
        instructionMnemonicsLines = []
        instructionMnemonicsLines.append(['*=0900'])
        for line in dataLines:
            hexaStringLines.append(self.fromDecimalString_toHexCode(line))
        binaryCode = self.buildBinaryCode(hexaStringLines)
        for toPrintLine in hexaStringLines:
            instructionMnemonicsLines.append(self.fromHexCode_tomnemonicCode(toPrintLine))
        self.printMnemonics(instructionMnemonicsLines)
        self.write_fileMnemonics(writeFilename,instructionMnemonicsLines)
        print("Writing File: ",writeFilename)
        print("Binary Code",binaryCode)


    def printDataLines(self,dataLines):
        for line in dataLines:
            print (line)

    def printMnemonics(self,instructionMnemonicsLines):
        for line in instructionMnemonicsLines:
            for instruction in line:
                print (instruction)

def main():
    dp = DataParser()
    if len(sys.argv) != 3:
        print ("Invalid amount of arguments, call it as:")
        print ("mainParser fileWithBasicCode.bas fileToHaveASMCode.asm")
    else:
        pythonProgramFileName = sys.argv[0]
        readFilename = sys.argv[1]
        writeFilename = sys.argv[2]
        dp.parseDataFile(readFilename,writeFilename)
    # readFilename = "004_byte01.bas"
    # writeFilename = "003_byte01.asm"
    # print(readFilename, writeFilename)
    # dp.parseDataFile(readFilename, writeFilename)


if __name__ == "__main__":
    main()