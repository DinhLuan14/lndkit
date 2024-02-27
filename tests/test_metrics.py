from lndkit import compute_score_multi_gts, compute_f1_score, compute_exact_score

if __name__ == "__main__":

    print(
        "f1_score:",
        compute_f1_score("hà nội", "Hà Nội tôi yêu")
    )
    print(
        "exact_score:",
        compute_exact_score("hà nội", "Hà Nội tôi yêu")
    )
    print(
        "exact_score with multiple ground truths:",
        compute_score_multi_gts("hà nội", ["Hà Thành", "Hà Nội"], metric="exact")
    )
    print(
        "f1_score with multiple ground truths:",
        compute_score_multi_gts("hà nội", ["Hà Thành", "Hà Lội", "Hà Nội tôi yêu"], metric="f1")
    )
