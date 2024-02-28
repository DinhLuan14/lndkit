import glob
import time

from tqdm import tqdm

from lndkit import cachef, hashf, read_json, timef, write_json


# test timef func
@timef
@cachef(["input_path"], cache_dir="test_cache")
def rwjson(input_path, output_path):
    print("read_json file", input_path)
    data = read_json(input_path)
    time.sleep(3)
    print(hashf("text"))
    print(data)
    print("write_json file")
    # write_json(data, output_path)


if __name__ == "__main__":
    timef(rwjson("tests/jsons/json1.json", ""))
    print("done 1\n----")
    jsons_path = glob.glob("tests/jsons/*")
    print(jsons_path)
    for jsn in tqdm(jsons_path):
        timef(rwjson(jsn, ""))
