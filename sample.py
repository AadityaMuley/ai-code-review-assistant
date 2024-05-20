def addition():
    a = 1
    b = 2
    return a + b

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def find_max(arr):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

class SampleClass:
    def __init__(self, value):
        self.value = value

    def increment(self):
        self.value += 1
        return self.value

def main():
    print("Factorial of 5:", factorial(5))
    print("Maximum in [1, 2, 3, 4, 5]:", find_max([1, 2, 3, 4, 5]))
    obj = SampleClass(10)
    print("Incrementing value:", obj.increment())

if __name__ == "__main__":
    main()
