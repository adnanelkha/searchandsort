def mergesort(data):
    if len(data) > 1: 
        mid = len(data)//2
        lefthalf = data[:mid]
        righthalf = data[mid:]
       
        mergesort(lefthalf)
        mergesort(righthalf)

        i = j = k = 0
 
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                data[k] = lefthalf[i]                
                i += 1
            else:
                data[k] = righthalf[j]
                j += 1
            k += 1
     
        while i < len(lefthalf):
            data[k] = lefthalf[i]
            i += 1
            k += 1
 
        while j < len(righthalf):
            data[k] = righthalf[j]
            j += 1
            k += 1
        
        return(data)
