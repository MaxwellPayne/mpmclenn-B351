# 1.
def sum_multiples(upper_bound):
    three, five = 3, 5
    
    def sum_arith_series(common_difference, until):
        n_terms = until / common_difference
        nth_term = common_difference * n_terms
        common_difference = float(common_difference)
        return (n_terms / 2.0) * (common_difference + nth_term)

    sum_threes = sum_arith_series(three, upper_bound)
    sum_fives = sum_arith_series(five, upper_bound)
    lcm = three * five
    common_term_sum = sum_arith_series(lcm, upper_bound)

    return sum_threes + sum_fives - common_term_sum

# 2.
def fib_recur(nth):
    n = nth
    if n in (0, 1):
        return n
    else:
        return fib_recur(n-1) + fib_recur(n-2)

def fib_iter(nth):
    if nth == 0: return 0
    
    result, to_add = 1, 0
    temp = 0
    for i in xrange(nth - 1):
        temp = result
        result = result + to_add
        to_add = temp

    return result

# 3.
def deriv(f, xVal):
    DELTA_X = 0.0000001
    return (f(xVal + DELTA_X) - f(xVal)) / DELTA_X

# 4.
def matrix_mult(matrix1, matrix2):
    product_matrix = []
    for nth_row, row in enumerate(matrix1):
        current_row_product = []
        for nth_col in xrange(len(matrix1)):
            col = map(lambda row_n: row_n.__getitem__(nth_col), matrix2)
            pairs = zip(row, col)
            current_row_product.append(sum(map(lambda pair: pair[0] * pair[1], pairs)))
        product_matrix.append(current_row_product)
    return product_matrix

def _main():
    print sum_multiples(10)
    print sum_multiples(1000)
    print fib_recur(8)
    print fib_iter(50)
    print deriv(lambda x: 2 * (x ** 3), 5)
    print matrix_mult([[1,2,3],[4,5,6]], [[7,8],[9,10],[11,12]])
    print matrix_mult([[2,4,1],[8,9,10],[1,3,2]], [[7,9,1],[3,3,2],[10,11,12]])

    # 5.
    from levenshtein import Levenshtein

    lev1 = Levenshtein("Jack is a very nice boy, isn't he?", "jack is a very nice boy is he")
    print lev1.distance()

if __name__ == '__main__':
    _main()

