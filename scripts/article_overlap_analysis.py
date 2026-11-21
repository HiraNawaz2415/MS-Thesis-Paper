"""Article-level overlap between ROCOv2 partitions and its effect on Test-final results (Reviewer 1, Round 2).

Reads only files the user already holds:
  license_information.csv   ROCOv2 release file: ID, PMCID, Attribution, Link
  train_prepared.csv, validation_prepared.csv, calibration_prepared.csv, test_final_prepared.csv
                            output of Notebook 02 (columns ID, label_C...)
  test_final_logits_fp32.csv  full-precision logits of the proposed VLM on Test-final (same row order)
  qhat_fp32.json            per-label conformal thresholds (label name -> q-hat) from the full-precision recalibration

Prints: (1) articles shared between partitions, (2) Micro/Macro-F1 of Test-final and of the subsets whose article does not
occur in Validation (and Validation or Calibration), (3) mean conformal coverage on the shared-article and other
Test-final images with image-level and article-level bootstrap intervals.

Usage:
  python article_overlap_analysis.py --data-dir <folder with the CSVs> --logits <test_final_logits_fp32.csv> --qhat <qhat_fp32.json>
Only the Python standard library is needed. Decision rule: positive if logit > 0 (probability > 0.5).
"""
import argparse
import csv
import json
import math
import random
from collections import Counter
from pathlib import Path

LABEL_NAMES = ["Abdomen", "Angiogram", "Breast", "Lower Extremity", "Magnetic Resonance Imaging", "Pelvis",
               "Positron-Emission Tomography", "Bone structure of cranium", "Vertebral column",
               "X-Ray Computed Tomography", "Ultrasonography", "Transverse", "Sagittal", "Chest", "Upper Extremity",
               "Plain x-ray", "Postero-Anterior", "Anterior-Posterior"]  # order of label_mapping.json


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sigmoid(z):
    return 1 / (1 + math.exp(-z)) if z >= 0 else math.exp(z) / (1 + math.exp(z))


def f1_scores(idx, Y, Z):
    tp = fp = fn = 0
    per = []
    for j in range(len(Y[0])):
        a = b = c = 0
        for i in idx:
            p, y = Z[i][j] > 0, Y[i][j]
            a += p and y
            b += p and not y
            c += (not p) and y
        tp, fp, fn = tp + a, fp + b, fn + c
        per.append(2 * a / (2 * a + b + c) if 2 * a + b + c else 0.0)
    return 2 * tp / (2 * tp + fp + fn), sum(per) / len(per)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--logits", required=True, type=Path)
    ap.add_argument("--qhat", required=True, type=Path)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()

    pmc = {r["ID"]: r["PMCID"] for r in read(a.data_dir / "license_information.csv")}
    parts = {n: read(a.data_dir / f"{n}_prepared.csv") for n in ["train", "validation", "calibration", "test_final"]}
    art = {n: [pmc[r["ID"]] for r in rows] for n, rows in parts.items()}
    sets = {n: set(v) for n, v in art.items()}

    print("Partition sizes:", {n: len(r) for n, r in parts.items()})
    for other in ["validation", "calibration", "test_final"]:
        k = sum(x in sets["train"] for x in art[other])
        print(f"{other}: images sharing an article with Train = {k}")
    tf = art["test_final"]
    in_val = [x in sets["validation"] for x in tf]
    in_cal = [x in sets["calibration"] for x in tf]
    print(f"Test-final images sharing an article with Validation: {sum(in_val)} / {len(tf)}")
    print(f"Test-final images sharing an article with Calibration: {sum(in_cal)} / {len(tf)}")

    rows = parts["test_final"]
    label_cols = [c for c in rows[0] if c.startswith("label_C")]
    Y = [[int(r[c]) for c in label_cols] for r in rows]
    lg = read(a.logits)
    Z = [[float(r[c + "_logit_fp32"]) for c in label_cols] for r in lg]
    assert len(Z) == len(Y), "logit rows must be in Test-final order"

    everything = list(range(len(rows)))
    no_val = [i for i in everything if not in_val[i]]
    no_val_cal = [i for i in everything if not in_val[i] and not in_cal[i]]
    for name, idx in [("all Test-final", everything), ("no Validation article", no_val),
                      ("no Validation or Calibration article", no_val_cal)]:
        mi, ma = f1_scores(idx, Y, Z)
        print(f"{name}: n={len(idx)} Micro-F1={mi:.4f} Macro-F1={ma:.4f}")

    q = json.loads(a.qhat.read_text())
    cov = []
    for i in everything:
        c = 0
        for j, name in enumerate(LABEL_NAMES):
            z = Z[i][j]
            s = sigmoid(-z) if Y[i][j] == 1 else sigmoid(z)  # LAC score: 1-p for y=1, p for y=0
            c += s <= q[name]
        cov.append(c / len(LABEL_NAMES))
    print(f"Mean coverage: {sum(cov) / len(cov):.4f}")
    sh = [c for c, s in zip(cov, in_cal) if s]
    ot = [c for c, s in zip(cov, in_cal) if not s]
    print(f"  sharing an article with Calibration: n={len(sh)} {sum(sh) / len(sh):.4f}; other: n={len(ot)} {sum(ot) / len(ot):.4f}")

    by_art = {}
    for i, x in enumerate(tf):
        by_art.setdefault(x, []).append(cov[i])
    keys = list(by_art)
    # One seeded generator; image-level resampling first, then article-level (this order reproduces the values
    # reported in the manuscript: image-level 0.8992-0.9062 and article-level 0.8985-0.9063 with seed 42, B = 2000).
    random.seed(a.seed)
    img_b = []
    for _ in range(a.boot):
        v = [random.choice(cov) for _ in cov]
        img_b.append(sum(v) / len(v))
    art_b = []
    for _ in range(a.boot):
        s = n = 0
        for _ in keys:
            k = by_art[random.choice(keys)]
            s, n = s + sum(k), n + len(k)
        art_b.append(s / n)
    for name, b in [("image-level", img_b), ("article-level", art_b)]:
        b.sort()
        print(f"  95% bootstrap interval ({name}): {b[49]:.4f} - {b[1949]:.4f}  (percentiles 2.5 / 97.5 of {a.boot})")
    print("Articles with more than one Test-final image:", sum(v > 1 for v in Counter(tf).values()))
    # The manuscript's headline image-level interval (0.8990-0.9061) comes from the separate analysis script of the
    # Round 1 revision (numpy bootstrap) and is not recomputed here.


if __name__ == "__main__":
    main()
