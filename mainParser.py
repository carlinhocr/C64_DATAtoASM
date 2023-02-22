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

def main():
    dp = DataParser()
    instructionDecimal = "165"
    instructionHex = dp.codeDecimalTOhex(instructionDecimal)
    instructionFull = dp.instructionTobytes(instructionHex)
    print(instructionFull)

if __name__ == "__main__":
    main()