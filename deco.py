#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps, lru_cache


def disable(func):
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''

    @wraps(func)
    def wrapper(*args):
        if hasattr(func, '__wrapped__'):
            return func.__wrapped__(*args)
        return func(*args)
    return wrapper


def decorator(func):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # example of `update_wrapper` use
    return update_wrapper(wrapper, func)


def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''

    @wraps(func)
    def wrapper(*args):
        wrapper.calls += 1
        return func(*args)

    wrapper.calls = 0
    return wrapper


def memo(func):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''

    @wraps(func)
    @lru_cache()
    def wrapper(*args):
        result = func(*args)
        wrapper.__dict__.update(vars(func))
        return result
    return wrapper


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''
    @wraps(func)
    def wrapper(x, *args):
        return x if not args else func(x, wrapper(*args))

    return wrapper


def trace(trace_line='____'):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''
    def top_wrapper(func):
        indent = 0

        @wraps(func)
        def wrapper(*args):
            nonlocal indent
            func_name = func.__name__
            func_args = ','.join(map(str, args))

            if indent == 0:
                print('--> {func_name}({func_args})'.format(
                    func_name=func_name,
                    func_args=func_args
                ))
            else:
                print('{tabulator} --> {func_name}({func_args})'.format(
                    tabulator=trace_line * indent,
                    func_name=func_name,
                    func_args=func_args
                ))
            indent += 1
            result = func(*args)
            indent -= 1
            print('{tabulator} <-- {func_name}({func_args}) == {result}'.format(
                tabulator=trace_line * indent,
                func_name=func_name,
                func_args=func_args,
                result=result
            ))
            return result
        return wrapper
    return top_wrapper


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")
    # print("foo cache: {}".format(foo.cache_info()))

    print(bar(4, 4))
    print(bar(4, 4))
    print(bar(4, 4))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")
    # print("bar cache info: {}".format(bar.__wrapped__.cache_info()))

    print(fib.__doc__)
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
