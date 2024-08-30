for i in range(2, 10):
    for j in range(2, i):
        if i % j == 0:
            print(i, 'equals', j, '*', i//j)
            break
    
    else:
        print(i, 'is a prime number')