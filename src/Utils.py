def signedByteToInt(val):
    return val if val < 128 else val - 256  

def intToSignedByte(val):
    return val if val >= 0 else val + 256

def signedByteToIntAt(ba,index):
    return signedByteToInt(ba[index])

def intToSignedByteAt(ba,index,val):
    ba[index] = intToSignedByte(val)
