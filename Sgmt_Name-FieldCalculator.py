rec=0 
def autoIncrement(): 
    global rec 
    pStart = 1 
    pInterval = 1 
    if (rec == 0): 
        rec = pStart 
    else: 
        rec += pInterval
    reczfill = str(rec).zfill(3)
    return reczfill