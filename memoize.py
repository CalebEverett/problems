from functools import partial, wraps
from collections import Counter


def decorator_with_kwargs(decorator):
    @wraps(decorator)
    def wrapper(func=None, **k):
        if func is None:
            return partial(decorator, **k)
        return decorator(func=func, **k)

    return wrapper


@decorator_with_kwargs
def memoize(func=None, max_results=10):
    counter_results = Counter()
    counter_other = Counter()
    results = {}

    @wraps(func)
    def wrapper(*a, **k):

        # if the result in not in the map, calc it and update map and counters
        if a not in results:
            result = func(*a)

            # add result to map if there are empty slots
            if len(results.keys()) < max_results:
                results[a] = result
                counter_results.update([a])

            # if the count of the current result is greater than or equal to the count
            # of the result stored with the lowest count, move the count of the last result
            # to the other counter, add the count of the current result to the result counter
            # and update the results map
            else:
                last_result = counter_results.most_common(max_results)[-1]
                counter_other.update([a])
                if counter_other[a] >= last_result[1]:
                    counter_other.update({last_result[0]: last_result[1]})
                    counter_results.update({a: counter_other[a]})

                    del counter_results[last_result[0]]
                    del counter_other[a]

                    del results[last_result[0]]
                    results[a] = result

        # if the result is in the map, just update the results counter
        else:
            counter_results.update([a])

        return results[a]

    return wrapper


@memoize(max_results=3)
def memoized_func(*args):
    return "result"


if __name__ == "__main__":
    for i in range(5):
        for j in range(5):
            memoized_func(j, "two", "three")
    pass
