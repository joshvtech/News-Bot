from datetime import datetime

time = datetime.now().replace(microsecond=0)

def getTime():
    return(datetime.now().replace(microsecond=0) - time)
