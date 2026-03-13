# Copilot coding agent instructions

## General goals
- Make sure that all the files in the Pull Request form a coherent whole.
- When you are unsure, ask clarifying questions.

## Pull requests & reviews
- Do *not* summarize the pull request.
- Leave **comments in French**.
- Use a **gentle, positive tone** in all review feedback.
- Favor actionable suggestions, and explain the “why” briefly.

## Python quality guidelines
- **Type all Python functions**: add type hints for parameters and
  return types.  If the return type is `None`, it must *not* not be
  declared.
- Use the PEP 695 syntax (Python >= 3.12).
- **Documentation**: every function that is not a test must have **at
  least one line of documentation** (docstring).
  - If a function has no docstring, suggest a very short one (one sentence) that states its purpose.
- **Factorization / DRY**:
  - Keep code well factorized and avoid repetition.
  - Extract helpers for repeated logic.
  - Prefer clear, reusable functions over copy/paste blocks.
- Ideally, lines of code should not exceed 80 chars.  Lines up to 100
  chars are tolerated; lines with more than 100 chars are forbidden.

## Style & maintainability
- Keep naming consistent and descriptive.
- Prefer pure functions when possible.
- Add or adjust tests when behavior changes.
- Update documentation when introducing new behavior.
