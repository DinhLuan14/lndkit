import functools
import inspect
import os.path as osp

from .utils import dump_json_or_pickle, hashf, load_json_or_pickle

DEFAULT_CACHE_DIR = osp.join(osp.expanduser("~"), ".cache/lndkit/av")


def get_arg_names(func):
    return inspect.getfullargspec(func).args


def cachef(keys, cache_dir=None):
    cache_dir = DEFAULT_CACHE_DIR if cache_dir is None else osp.join(osp.expanduser("~"), cache_dir)

    def decorator_cachef(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            assert isinstance(keys, (list, tuple))
            arg_names = get_arg_names(func)

            def get_key_value(key):
                if key in arg_names:
                    return args[arg_names.index(key)]
                if key in kwargs:
                    return kwargs[key]

            values = [get_key_value(key) for key in keys]

            # If keys not provide, simply run the function
            if not keys:
                return func(*args, **kwargs)

            key_id = hashf(values)  # Assuming 'hashf' generates a unique hash
            func_id = hashf(inspect.getsource(func))
            key_names = "_".join(keys)
            cache_path = osp.join(
                cache_dir,
                f"{func.__name__}_{func_id}",
                f"{key_names}_{key_id}.pkl",
            )
            if osp.exists(cache_path):
                return load_json_or_pickle(cache_path)
            result = func(*args, **kwargs)
            dump_json_or_pickle(result, cache_path)
            return result

        return wrapper

    return decorator_cachef
