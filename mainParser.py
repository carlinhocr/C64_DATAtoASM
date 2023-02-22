class DataParser(object):

    def __init__(self):
        pass

    def codeDecimalTOhex(self,instructionDecimal):
        decHex = {"165": "A5",
                  "120": "78"}
        return hex(int(instructionDecimal))[2:].upper() #[2:] to strip the 0x from the string
        pass

    def instructionTobytes(self,instructionHex):
        instruction = {
                        "A5":[1,"LDA","zeropage","A5"], # number of bytes that follow, mnemonic, memory addressing mode, hex code
                        "78":[0,"SEI","implied"]
                       }
        return instruction[instructionHex.upper()]

    def fromDecimalString_toHexCode(self):
        #get a list of strings with instructions and bytes
        #parse to a list of isntruction code and paramenters as a sublist according to its memory addresing
        #return list of strings with sublists of instructions and parameters
        pass

    def fromHexCode_tomnemonicCode(self):
        #get a list of strings with sublists of instructions and parameters
        #proper format it as mnemonics and $ and # formatting
        pass

    def prepareCodeForParsing(self,codeString):
        #strip the 10 DATA
        #parse the comma separated string and add to a list of strings
        #return the list of strings
        pass

def main():
    dp = DataParser()
    instructionDecimal = "165"
    instructionHex = dp.codeDecimalTOhex(instructionDecimal)
    instructionFull = dp.instructionTobytes(instructionHex)
    print(instructionFull)

if __name__ == "__main__":
    main()