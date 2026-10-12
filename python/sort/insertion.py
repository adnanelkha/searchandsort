def insertion(data):
    datalen = len(data)
    for i in range(1, datalen):
        if datalen <= 1:
            return
        for i in range(1, datalen):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j+1] = data[j]
                j -= 1
            data[j+1] = key
    return(data)