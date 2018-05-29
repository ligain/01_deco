#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps


def disable():
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    return


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
    func.calls = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    return wrapper


def memo():
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''
    return


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''
    @wraps(func)
    def wrapper(x, *args):
        return x if not args else func(x, wrapper(*args))

    return wrapper


def trace():
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
    return


# @memo
# @countcalls
# @n_ary
# def foo(a, b):
#     return a + b
#
#
# @countcalls
# @memo
# @n_ary
# def bar(a, b):
#     return a * b
#
#
# @countcalls
# @trace("####")
# @memo
# def fib(n):
#     """Some doc"""
#     return 1 if n <= 1 else fib(n-1) + fib(n-2)

@decorator
@countcalls
def foo(a, b):
    '''Docstring'''
    return a + b


@countcalls
def bar(a, b):
    return a * b


def main():
    print(foo(4, 3))
    # print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")
    print("foo doc: {}, foo name: {}".format(foo.__doc__, foo.__name__))
    #
    # print(bar(4, 3))
    # print(bar(4, 3, 2))
    # print(bar(4, 3, 2, 1))
    # print("bar was called", bar.calls, "times")
    #
    # print(fib.__doc__)
    # fib(3)
    # print(fib.calls, 'calls made')

    ############


if __name__ == '__main__':
    main()
