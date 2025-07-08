import re
import json
import random

# def extract_answer(prediction):
#     """Extract the equation from the solution string."""
#     # Remove everything before the first "Assistant:"
#     if "Assistant:" in prediction:
#         prediction = prediction.split("Assistant:", 1)[1]
#     elif "<|im_start|>assistant" in prediction:
#         prediction = prediction.split("<|im_start|>assistant", 1)[1]
#     else:
#         return None
#     prediction = prediction.split('\n')[-1]

#     answer_pattern = r'<answer>(.*?)</answer>'
#     match = re.finditer(answer_pattern, prediction)
#     matches = list(match)
#     if matches:
#         final_answer = matches[-1].group(1).strip()
#     else:
#         final_answer = None
    
#     return final_answer

# def extract_answer(text):
#     matches = re.findall(r'<answer>(.*?)</answer>', text, re.DOTALL)
#     return matches[-1].strip() if matches else None

def extract_last_complete_json(s):
    # Stack to keep track of opening and closing braces
    stack = []
    last_json_start = None
    last_json_str = None

    for i, char in enumerate(s):
        if char == "{":
            stack.append(i)
            if last_json_start is None:
                last_json_start = i
        elif char == "}":
            if stack:
                start = stack.pop()
                if not stack:
                    # Complete JSON object found
                    last_json_str = s[last_json_start : i + 1]
                    last_json_start = None

    # Load the last JSON object
    if last_json_str:
        try:
            return json.loads(last_json_str.replace("\n", ""))
        except json.JSONDecodeError:
            pass

    return None

def extract_solution(answer):
    return json.loads(answer)["solution"]

def compute_cell_acc(solution, solution_gt, do_print=False):
    cell_cnt = 0
    for k, v in solution_gt.items():
        cell_cnt += len(v)
    
    item2house = {}
    for k, v in solution_gt.items():
        for vk, vv in v.items():
            item2house[vv] = v
            break
    
    correct_cnt = 0
    for k, v in solution.items():
        # invalid house
        if k not in solution_gt:
            continue
        v_gt = None
        for vk, vv in v.items():
            if v_gt is None:
                v_gt = item2house.get(vv, None)
                if v_gt is None:
                    break
            if vk in v_gt and v_gt[vk] == vv:
                correct_cnt += 1
    if do_print:
        print(f"solution: {solution}")
        print(f"solution_gt: {solution_gt}")
        print(f'correct_cnt: {correct_cnt}, cell_cnt: {cell_cnt}')
    return correct_cnt / cell_cnt
    

def compute_score(solution_str, ground_truth, method='strict', format_score=0.1, score=1.):
    """The scoring function for countdown task.
    
    Args:
        solution_str: the solution text
        ground_truth: dictionary containing target number and available numbers
        method: the method to extract the solution
        format_score: the score for correct format but wrong answer
        score: the score for the correct answer
    """
    try:
        answer = extract_last_complete_json(solution_str)
        if answer is None:
            return 0
        pred = answer["solution"]
        gt = json.loads(ground_truth)
        score = compute_cell_acc(pred, gt, do_print=True)
    except Exception as e:
        print(f"Error extracting solution: {e}")
        return 0
    return score + format_score