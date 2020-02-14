# def factorize(x):
#     """
#     Factorize positive integer and return its factors.
#     :type x: int,>=0
#     :rtype: tuple[N],N>0
#     """
#     if not isinstance(x, int):
#         raise TypeError('Wrong input type, must be "int"!')
#     if x < 0:
#         raise ValueError('"x" must be not negative!')
#
#     for candidate in range(2, x):
#         if x % candidate == 0:
#             return (candidate, ) + factorize(x // candidate)
#
#     return x,


def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    return None