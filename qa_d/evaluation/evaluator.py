import csv
import os

from qa_d.prompting.llama_prompter import LlamaPrompter

quest_path = os.path.join(os.path.dirname(__file__), "..", "qa.csv")
result_path = os.path.join(os.path.dirname(__file__), "..", "results")
models = ['gemma-2-27b-it', 'Llama-3.3-70B-Instruct'.lower(), 'gpt-4o-2024-11-20']
evaluator_llm = LlamaPrompter()

sys_msg_scoring = f"Your task is to evaluate answers given by another LLM. You are provided the question, the ground truth answer and the answer given by the other LLM. Given this information, please return a score symbolising the quality of the answer and its closeness to the ground truth. The score should range from 0 to 5, where 5 is the best and 0 is used when the LLM could not provide any answer."
sys_msg_bin = f"Your task is to evaluate answers given by another LLM. You are provided the question, the ground truth answer and the answer given by the other LLM. Given this information, please return True or False depending on whether or not the answer aligns with the ground truth."


def get_model_answer(model: str, question: str) -> str:
    with open(f"{result_path}/{model}.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["question"] == question:
                return row["model_answer"]
    return ""


# Evaluate the results generated by the different LLMs using an evaluator LLM.
# Differentiate between binary evaluation (Is the answer correct - True/False) and a score-based evaluation (What is the quality of the answer on a scale of 0 (= no answer) to 5 (= best answer)
def evaluate_models(bin_res=True):
    if bin_res:
        sys_msg = sys_msg_bin
        file_n = "binary"
    else:
        sys_msg = sys_msg_scoring
        file_n = "scoring"

    for m in models:
        scores = []
        with open(quest_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                quest = row[0]
                gt_ans = row[1]
                m_ans = get_model_answer(m, quest)
                user_msg = f"\nQuestion: {quest}\nGround Truth: {gt_ans}\nLLM Answer: {m_ans}\nResult:"
                score = evaluator_llm.prompt_model(sys_msg, user_msg)
                scores.append((quest, gt_ans, m_ans, score))
        with open(f"{result_path}/{m}_{file_n}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["question", "ground_truth", "model_answer", "score"])
            writer.writerows(scores)


if __name__ == "__main__":
    evaluate_models()
    evaluate_models(False)
