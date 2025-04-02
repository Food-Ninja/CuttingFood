import csv
import os
import re

result_path = os.path.join(os.path.dirname(__file__), "..", "results")
models = ['gemma-2-27b-it', 'Llama-3.3-70B-Instruct'.lower(), 'gpt-4o-2024-11-20']
file_ext_bin = "binary"
file_ext_score = "scoring"


def get_binary_from_text(text: str) -> bool:
    cont_true = cont_false = False
    if "true" in text.lower():
        cont_true = True
    if "false" in text.lower():
        cont_false = True
    assert cont_true != cont_false
    return cont_true


def get_score_from_text(text: str) -> int:
    match = re.search(r'\b\d+\b', text)
    if match is None:
        return -1
    else:
        return int(match.group())

def evaluate_binary_results():
    for m in models:
        correct = 0
        rows = 0
        with open(f"{result_path}/{m}_{file_ext_bin}.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                rows += 1
                if get_binary_from_text(row[3]):
                    correct += 1
            accuracy = correct / rows
        print(f'For {m}: {correct} answers are correct. Accuracy = {accuracy}\n')


def evaluate_scoring_results():
    for m in models:
        total = 0
        rows = 0
        no_score = 0
        with open(f"{result_path}/{m}_{file_ext_score}.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                score = get_score_from_text(row[3])
                if score == -1:
                    no_score += 1
                else:
                    rows += 1
                    total += score
            avg = total / rows
        print(f'For {m}, the average score is {avg}. However, {no_score} answers were not given a score by the evaluating LLM\n')


if __name__ == "__main__":
    evaluate_binary_results()
    evaluate_scoring_results()
