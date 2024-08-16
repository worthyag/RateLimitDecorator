"""
Rate Limiting

A decorator that limits how often a function can be called within a certain time frame.
The decorator enforces a rate limit, allowing the function to be called only a certain number 
of times within a specified interval.

An example use case: Using this to prevent excessive API calls or limit the rate of sending emails.
"""
import time
import functools
from functools import wraps


def within_time_limit(current_time, time_interval, timestamp) -> bool:
    time_lapse = current_time - timestamp
    return time_lapse < time_interval


def rate_limit(max_call: int = 3, time_interval: int = 3):
    def decorator(func):
        # Dictionary that stores the number of times a particular function has been called.
        # {function_name: [timestamps]}, the value is a list of timestamps, the length of the
        # array corresponds to call count, and the timestamps can be used to determine the time frame
        call_count = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()

            if func.__name__ not in call_count.keys():
                call_count[func.__name__] = [current_time]
                return func(*args, **kwargs)
            else:
                # Using functools.partial to fix the current_time and time_interval parameters.
                within_time_limit_partial = functools.partial(within_time_limit,
                                                              current_time,
                                                              time_interval)

                # Checking whether the number of calls within the interval exceeds the limit.
                call_count[func.__name__] = list(filter(within_time_limit_partial,
                                                        call_count[func.__name__]))

                if len(call_count[func.__name__]) >= max_call:
                    print(f"Function '{func.__name__}()' has "
                          "exceeded the max number of calls.")
                    print(call_count[func.__name__])
                else:
                    call_count[func.__name__].append(current_time)
                    return func(*args, **kwargs)

        return wrapper
    return decorator


@rate_limit(3, 5)
def printName(name: str) -> None:
    print(name.title())


for i in range(5):
    printName("Worthy")
    time.sleep(0.75)
