import functools

# Works, but I just realized now that it's not what I need D:
#
# def fixed_arguments(**kwargs):
#     """
#     A simple decorator to be used when we want to use multiprocessing -- we can
#     only pass one argument to each function call, but sometimes we need to pass
#     additional fixed arguments to the function!
#     """
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args):
#             # This uses the **kwargs from our outermost dectorator
#             return func(*args, **kwargs)

#         return wrapper

#     return decorator

# SADNESS!
#
# Turns out we can't use decorators on functions passed to multiprocessing.
#
# def argument_tuple(func):
#     """
#     Multiprocessing map can only pass a single argument to the function -- but
#     sometimes we need multiple arguments! The workaround is to pass a tuple of
#     arguments. This decorator just unpacks that tuple when the function is
#     called.
#     """
#     def wrapper(argtuple):
#         return func(*argtuple)
#     return wrapper