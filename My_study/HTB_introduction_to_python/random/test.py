import time

for i in range(101):
    break
    print(f"\rDownloading...{i}", flush=True, end="")
    time.sleep(0.005)
print()


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def test(func, x, y):
    return func(x, y)


def greetings(name):
    def hello():
        return f"Hello: {name}."

    return hello


sss = "ABCDEFG"
print(sss[:-1])
print(f"sum: {test(add,5,4)}\nsubtract: {test(subtract,5,4)}")
print(greetings("ahmad"))
