def binary_search(data, target):
    low=0
    high=len(data)-1
    found=False
    while low <= high:
        mid=(high+low)//2
        if data[mid] == target:
            return target
        elif data[mid] > target:
            high=mid-1
        elif data[mid] < target:
            low=mid+1
    return -1
