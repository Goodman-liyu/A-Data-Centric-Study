import rich
from rich.syntax import Syntax
from rich.rule import Rule

from verl.utils.reward_score.coder1 import code_exec

def test_code(note, code, stdin=None, stdout=None, expect_error=False):
    rich.print(Rule(note))
    rich.print(Syntax(code, "python", word_wrap=True))
    succ, output = code_exec(code, stdin=stdin)
    print(f"{succ = }")
    if not succ:
        print(f"Error:\n{output}")
    else:
        print(f"{output = }")
    if expect_error:
        assert not succ, "Expecting a failure"
    else:
        assert succ, "Expecting a success"
        if stdout is not None:
            assert output == stdout, f"Expecting {stdout = } but got {output = }"

test_code("functionality: test normal", "print('hello world')", stdout="hello world\n")
test_code("functionality: test numpy", r"""import numpy as np
print(np.ones((6,)).sum())""", stdout="6.0\n")
test_code("functionality: test stdin", "print(input())", stdin="hello world", stdout="hello world\n")
test_code("functionality: test error", "print(1/0)", expect_error=True)
