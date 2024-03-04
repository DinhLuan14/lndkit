from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm


def threadsf(func, data, workers=4):
    """
    Executes a function across multiple threads, each thread can execute the function
    with multiple arguments unpacked from a tuple or list.

    Parameters:
    - func: The function to execute, which accepts multiple arguments.
    - data: A list of dictionaries with the format [{"unique_key": (arg1, arg2, arg3)}, ...].
    - workers: The number of threads to use.

    Returns:
    - A dictionary with the format {"unique_key_1": output1, "unique_key_2": output2, ...}.
    """

    def worker(item):
        unique_key, args = list(item.items())[0]
        output_value = func(*args)
        return unique_key, output_value

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(worker, item) for item in data]

        results = {}
        for future in tqdm(as_completed(futures), total=len(data), desc="Processing"):
            unique_key, output_value = future.result()
            results[unique_key] = output_value
    return results
