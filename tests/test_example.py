import glob
import time

from tqdm import tqdm

from lndkit import cachef, hashf, read_json, timef, write_json


# test timef func
@timef
@cachef(["input_path", "output_path"], cache_dir="test_cache")
def rwjson(input_path, output_path):
    print("read_json file", input_path)
    data = read_json(input_path)
    time.sleep(3)
    print(hashf("text"))
    print(data)
    print("write_json file")
    write_json([data], output_path, format_type="both", sample=1)


if __name__ == "__main__":
    timef(rwjson("tests/jsons/json1.json", "tests/json_write/test_dump"))
    print("done 1\n----")
    jsons_path = glob.glob("tests/jsons/*")
    print(jsons_path)
    for i, jsn in enumerate(tqdm(jsons_path)):
        timef(rwjson(jsn, f"tests/json_write/test_dump{i}"))
