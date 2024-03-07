import json
import random


def read_json(file_path):
    with open(file_path, "r") as f:
        if file_path.endswith(".jsonl"):
            data = [json.loads(line) for line in f]
        else:
            data = json.load(f)
    return data


def write_json(data, name, format_type="both", sample=None, info=True):
    assert format_type in ["both", "json", "jsonl"]

    output_json = f"{name}.json"
    output_jsonl = f"{name}.jsonl"
    output_sample_json = f"{name}_sample_{sample}.json" if sample is not None else None
    output_sample_jsonl = f"{name}_sample_{sample}.jsonl" if sample is not None else None

    # write  file JSON
    if format_type in ["json", "both"]:
        with open(output_json, "w", encoding="utf-8") as file:
            if info:
                json.dump({"__count__": len(data), "data": data}, file, ensure_ascii=False, indent=3)
            else:
                json.dump(data, file, ensure_ascii=False, indent=3)
        if sample is not None and sample > 0:
            data_sample = random.sample(data, min(sample, len(data)))
            with open(output_sample_json, "w", encoding="utf-8") as file:
                if info:
                    json.dump({"__count__": len(data_sample), "data": data_sample}, file, ensure_ascii=False, indent=3)
                else:
                    json.dump(data_sample, file, ensure_ascii=False, indent=3)

    # write file JSONL
    if format_type in ["jsonl", "both"]:

        def write_jsonl(file_path, data_out):
            with open(file_path, "w", encoding="utf-8") as file:
                for element in data_out:
                    json.dump(element, file, ensure_ascii=False)
                    file.write("\n")

        write_jsonl(output_jsonl, data)
        if sample is not None and sample > 0:
            data_sample = random.sample(data, min(sample, len(data)))
            write_jsonl(output_sample_jsonl, data_sample)
