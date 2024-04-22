---
layout: blog_post
title: Python decorators for fun and profit
date: 2024-04-22
last_modified: 2024-04-22
---
Two python functions:

```
def print_status_and_execute(f):
    print("running function " + f.__qualname__)
    return f

def add(x, y):
    return x+y
```

You might want to wrap them like:

```
status_printing_add = print_status_and_execute(add)
```

Which is _kind of_ ok, except that now you have to change all your code wherever you used to use `add` to use the new `status_printing_add` function.

Instead, you can just decorate the function definition of `add` like so:
<!--more-->

```
def print_status_and_execute(f):
    def fn(*args, **kwargs):
        print("running function " + f.__qualname__)
        return f(*args, **kwargs)
    return fn

@print_status_and_execute
def add(x, y):
    return x+y
```

And now every instance of add behaves as if it is automatically transformed:
`add(a, b) -> print_status_and_execute(add)(a, b)`

You can even make decorators themselves depend on arguments, though it requires an extra level of abstraction:

```
def print_n_times(n):
    def decorator(f):
        def fn(*args, **kwargs):
            for i in range(n):
                print(*args)
                print(**kwargs)
            return f(*args, **kwargs)
        return fn
    return decorator

@print_n_times(5)
def say_hello(name):
    print("hello " + name)
```

Or do fancier things, like create and maintain extra data structures available to their context across function calls:

```
def memoize(fn):
    prev_res = {}
    def mem(num):
        if num in prev_res.keys():
            return prev_res[num]
        else:
            val = fn(num)
            prev_res[num] = val
            return val
    return mem

@memoize
def fibb(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return fibb(n-1) + fibb(n-2)
```