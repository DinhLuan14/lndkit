import json
import os
import os.path as osp
import pickle
import time

import xxhash


def timef(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:0.2f} seconds to execute.")
        return result

    return wrapper


def hashf(x):
    """Return an hex digest of the input"""
    return xxhash.xxh64(pickle.dumps(x), seed=0).hexdigest()


def mkdir_or_exist(dir_name):
    return os.makedirs(dir_name, exist_ok=True)


def dump_json_or_pickle(obj, fname, ensure_ascii=False):
    """
    Dump an object to a file, support both json and pickle
    """
    mkdir_or_exist(osp.abspath(os.path.dirname(osp.abspath(fname))))
    if fname.endswith(".json") or fname.endswith(".jsonl"):
        with open(fname, "w") as f:
            json.dump(obj, f, ensure_ascii=ensure_ascii)
    elif fname.endswith(".pkl"):
        with open(fname, "wb") as f:
            pickle.dump(obj, f)
    else:
        raise NotImplemented(fname)


def load_json_or_pickle(fname):
    """
    Load an object from a file, support both json and pickle
    """
    if fname.endswith(".json") or fname.endswith(".jsonl"):
        with open(fname, "r") as f:
            return json.load(f)
    else:
        with open(fname, "rb") as f:
            return pickle.load(f)
