import collections
import string

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_answer(answer):
    answer = answer.lower()
    answer = answer.replace("-", " ").replace("–", " ").replace("/", " ").replace("\n", ". ")
    normed_answer = ""
    for w in answer.split():
        w = w.strip(string.punctuation)
        if not is_number(w):
            w = "".join(ch for ch in w if ch not in string.punctuation)
        else:
            w = normalize_number_str(w)
        normed_answer += w + " "
    normed_answer = normed_answer.strip()
    return normed_answer


def normalize_number_str(number_str):
    number_str = number_str.replace(",", ".")
    count_dot = number_str.count(".")
    if count_dot > 1:
        number_str = number_str.replace(".", "")
    elif count_dot == 1:
        dot_id = number_str.index(".")
        count_digits = len(number_str) - dot_id - 1
        if count_digits % 3 == 0:
            number_str = number_str.replace(".", "")
        else:
            number_str = str(round(float(number_str), 1))

    return number_str


def is_number(word):
    valid_str = "0123456789.,"
    return all(c in valid_str for c in word)


def match_numbers(gt_numbers, pred_numbers):
    gt_numbers = set(gt_numbers)
    pred_numbers = set(pred_numbers)
    if not gt_numbers or gt_numbers.intersection(pred_numbers):
        return True

    return False


def contain_numbers_only(answer):
    words = answer.split()
    numbers = [w for w in words if is_number(w)]
    return len(words) == len(numbers)


def get_gts_focus_numbers(gts):
    gts_normed = [normalize_answer(gt) for gt in gts]
    gts_numbers = [gt for gt in gts_normed if contain_numbers_only(gt)]

    gts_focus_numbers = []
    for gtn in gts_numbers:
        numbers = [w for w in gtn.split() if is_number(w)]
        is_focus_number = True
        for n in numbers:
            if not all(n in gt for gt in gts):
                is_focus_number = False
                break
        if is_focus_number:
            gts_focus_numbers.append(gtn)

    return gts_focus_numbers


def compute_exact_score(pred, gt):
    assert gt.strip()

    pred = normalize_answer(pred)
    gt = normalize_answer(gt)

    exact_score = int(pred == gt)
    return exact_score


def compute_f1_score(pred, gt):
    assert gt.strip()

    pred = normalize_answer(pred)
    gt = normalize_answer(gt)

    pred_words = pred.split()
    gt_words = gt.split()

    pred_numbers = [w for w in pred_words if is_number(w)]
    gt_numbers = [w for w in gt_words if is_number(w)]

    if len(gt_words) == len(gt_numbers) and sorted(gt_numbers) == sorted(pred_numbers):
        return 1

    if not match_numbers(gt_numbers, pred_numbers):
        return 0

    common = collections.Counter(pred_words) & collections.Counter(gt_words)
    num_same = sum(common.values())
    if num_same == 0:
        return 0

    precision = 1.0 * num_same / len(pred_words)
    recall = 1.0 * num_same / len(gt_words)
    f1_score = (2 * precision * recall) / (precision + recall)
    return f1_score


def compute_score_multi_gts(pred, gts, metric="f1"):
    assert metric in ["exact", "f1"]

    gts = set([gt for gt in gts if gt.strip()])
    assert gts

    if metric == "exact":
        score = max(compute_exact_score(pred, gt) for gt in gts)
    else:
        score = max(compute_f1_score(pred, gt) for gt in gts)

    return score


class ComputeCosine:
    def __init__(self, model_path):
        self.model = SentenceTransformer(model_path)

    def compute_score(self, s1, s2, exp=3):
        s1 = self.model.encode(s1, normalize_embeddings=True, show_progress_bar=False).reshape(1, -1)
        s2 = self.model.encode(s2, normalize_embeddings=True, show_progress_bar=False).reshape(1, -1)
        score = list(cosine_similarity(s1, s2) ** exp)[0]
        return score

    def score_with_mean(self, text, prompts=None, exponent=3, print_scores=True):
        prompts = [
            "Please improve the following text using the writing style of, maintaining the original meaning but altering the tone, diction, and stylistic elements to match the new style.Enhance the clarity, elegance, and impact of the following text by adopting the writing style of , ensuring the core message remains intact while transforming the tone, word choice, and stylistic features to align with the specified style.",
            "Please improve the following text using the writing style of, maintaining the original meaning but altering the tone, diction, and stylistic elements to match the new style.",
            "Please revise this text to enhance its clarity and impact, ensuring alignment with [insert desired style here] while preserving the original message. Aim for elegance and precision in tone and word choice.",
        ]
        scores = [self.compute_score(text, prompt, exponent) for prompt in prompts]
        if print_scores:
            for i, score in enumerate(scores, 1):
                print(f"Score mean {i}: ", score)
        return scores
