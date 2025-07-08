# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from concurrent.futures import ProcessPoolExecutor, TimeoutError
import re
from .qwen_math_eval_toolkit.parser import extract_answer as qwen_extract_answer
# from .qwen_math_eval_toolkit.grader import math_equal as qwen_math_equal
from functools import partial
from concurrent.futures import ProcessPoolExecutor, TimeoutError
import threading
import logging
from typing import Optional, Callable, Any
from functools import wraps
import random
import gc 
from math_verify import parse, verify

class GlobalProcessPool:
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self, max_workers: int = 16, reset_threshold: int = 100000):
        self.max_workers = max_workers
        self.reset_threshold = reset_threshold
        self.task_counter = 0
        self.executor: Optional[ProcessPoolExecutor] = None
        self.logger = logging.getLogger(__name__)
        self._initialize_executor()
    
    def _initialize_executor(self) -> None:
        """Initialize a new ProcessPoolExecutor and reset task counter."""
        if self.executor is not None:
            self.executor.shutdown(wait=False)
            self.executor = None
            gc.collect() 
        self.executor = ProcessPoolExecutor(max_workers=self.max_workers)
        self.task_counter = 0
        self.logger.warning(f"Initialized ProcessPoolExecutor with {self.max_workers} workers")
    
    @classmethod
    def get_instance(cls, max_workers: int = 16, reset_threshold: int = 100000) -> 'GlobalProcessPool':
        """Get or create the singleton instance of GlobalProcessPool."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(max_workers=max_workers, reset_threshold=reset_threshold)
        return cls._instance
    
    def submit(self, fn: Callable, *args, **kwargs) -> Any:
        """
        Submit a task to the executor with automatic recovery and periodic reset.
        
        Args:
            fn: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Future object representing the computation
        """
        try:
            if self.executor is None:
                with self._lock:
                    self._initialize_executor()
            return self.executor.submit(fn, *args, **kwargs)
        except (Exception, RuntimeError) as e:
            self.logger.warning(f"Process pool broken, recreating: {str(e)}")
            with self._lock:
                self._initialize_executor()
            return self.executor.submit(fn, *args, **kwargs)

# Create the global executor instance
global_executor = GlobalProcessPool.get_instance(max_workers=16)

def extract_last_boxed(text):
    """
    提取 LaTeX 文本中最后一个 \boxed 命令中的内容
    
    返回:
    - str: 最后一个 \boxed 中的内容。如果没有找到则返回 None
    """
    pattern = r'\\boxed\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}'
    
    # 找到所有匹配
    matches = list(re.finditer(pattern, text))
    
    # 如果找到匹配，返回最后一个的内容
    if matches:
        return matches[-1].group(0)
    return None

def extract_last_answer(text):
    """
    提取文本中 <answer> 标签中的内容
    
    返回:
    - str: <answer> 标签中的内容。如果没有找到则返回 None
    """
    # 正则表达式匹配 <answer> 标签中的内容
    pattern = r'<answer>(.*?)</answer>'
    
    # 使用 findall 查找所有匹配
    matches = re.findall(pattern, text)
    
    # 如果找到匹配，返回最后一个匹配的内容
    if matches:
        return matches[-1]  # 返回最后一个匹配
    return None

    
def extract_solution(solution_str):
    model_output= re.sub(r'^.*?<\|im_start\|>assistant', '<|im_start|>assistant', solution_str, flags=re.DOTALL,count = 1)
    stop_words = ["</s>", "<|im_end|>", "<|endoftext|>"] 
    for stop_word in stop_words:
        if stop_word in model_output:
            model_output = model_output.split(stop_word)[0].strip()
    
    # predict_answer = qwen_extract_answer(model_output, data_name="math")
    # extract_boxed_answer = extract_last_answer(model_output)
    extract_answer = extract_last_answer(model_output)
    if extract_answer is not None:
        predict_answer = qwen_extract_answer(extract_answer, data_name="math")
    else:
        predict_answer = None
    # True means the boxed answer is correct
    # if extract_boxed_answer is not None:
    if predict_answer is not None:
        return predict_answer, True
    else:
        return predict_answer, False


def hf_verify_with_try(gold, target):
    try:
        parsed_target = parse(target)    
        parsed_gold = parse(gold)
        return verify(gold=parsed_gold, target=parsed_target)
    except Exception as e:
        print(f"Gold: {gold} Target: {target} Error: {str(e)}")
        return False


def hf_math_equal_subprocess(gold, target, timeout_seconds=10):
    """
    使用 ProcessPoolExecutor 实现带超时的函数执行
    
    Args:
        gold: 参考答案
        target: 预测结果
        timeout_seconds: 超时时间(秒)
        
    Returns:
        bool: 执行结果,超时返回 False
    """
    try:
        # 提交任务到进程池
        future = global_executor.submit(hf_verify_with_try, gold=gold, target=target)
        # 等待结果,支持超时
        result = future.result(timeout=timeout_seconds)
        return result
    except TimeoutError:
        print(f"Timeout occurred for gold {gold} and target {target}.")
        return False
    except Exception as e:
        print(f"Gold: {gold} Target: {target} Error: {str(e)}")
        return False


import os 
# TODO: Might have problem in multi node ray cluster !!!!
reward_function_type = str(os.environ.get('REWORD_FUNCTION_TYPE', "mix"))
format_penalty_value = float(os.environ.get('FORMAT_PENALTY_VALUE', "-1"))

print(f"Reward function type: {reward_function_type}")
print(f"Format penalty value: {format_penalty_value}")

def compute_score(solution_str, ground_truth, method='strict'):
    """The scoring function for GSM8k.

    Reference: Trung, Luong, et al. "Reft: Reasoning with reinforced fine-tuning." Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2024.

    Args:
        solution_str: the solution text
        ground_truth: the ground truth
        method: the method to extract the solution, choices are 'strict' and 'flexible'
        format_score: the score for the format
        score: the score for the correct answer
    """
    extract_answer, is_boxed_matched = extract_solution(solution_str=solution_str)
    if is_boxed_matched == False:
        return 0
    
    if "\\boxed" not in extract_answer:
        boxed_answer = f"\\boxed{{{extract_answer}}}"
    else:
        boxed_answer = extract_answer
    
    if "\\boxed" not in ground_truth:
        boxed_ground_truth = f"\\boxed{{{ground_truth}}}"
    else:
        boxed_ground_truth = ground_truth
        
    
    # target = parse(boxed_answer)    
    # gold = parse(boxed_ground_truth)
    correct = hf_math_equal_subprocess(gold=boxed_ground_truth, target=boxed_answer)
    
    if reward_function_type == 'mix':
        if correct:
            box_match = 1.0
        else:
            box_match = 0
    elif reward_function_type == 'independent':
        if correct and is_boxed_matched:
            box_match = 1.0
        elif correct and not is_boxed_matched:
            box_match = 0.5
        elif not correct and is_boxed_matched:
            box_match = -0.5
        else:
            box_match = format_penalty_value
    else:
        raise ValueError(f"Invalid reward function type: {reward_function_type}")
            

    if random.random() < 0.005:
        # for 5% of the cases, print; otherwise, print nothing to accelerate the process 
        print(f"\n[Model Response]\n{solution_str}")
        print(f"\n[Ground Truth]\n{ground_truth}")
        print(f"\n[Is Boxed Matched]\n{is_boxed_matched}")
        print(f"\n[Extracted Answer]\n{extract_answer}")
        print(f"\n[Reward Score]\n{box_match}")
    # return {"score": box_match, "correctness": correct}
    return box_match
