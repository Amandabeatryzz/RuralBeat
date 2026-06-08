def fibonacci_otimizado(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

# Teste
fibonacci_otimizado(10)