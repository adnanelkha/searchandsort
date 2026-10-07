def bubble(data):
    datalen = len(data)
    for i in range(datalen-1):
        for j in range(datalen-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
    return(data)