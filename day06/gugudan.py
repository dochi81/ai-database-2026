#단순 기본 구구단

for x in range(2,10):
    for y in range (1,10):
        print(f'{x}x{y}) = {x*y:2d}', end=' ') 
    print()