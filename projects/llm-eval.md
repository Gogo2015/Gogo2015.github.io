---
layout: default
title: LLM Semantic Syntax Evaluation
---

# LLM Semantic Syntax Evaluation
**Repository:** [llm-semantic-syntax](https://github.com/Gogo2015/llm-semantic-syntax)
**Course:** CS 4392 — Programming Languages (Final Project)

## Project Overview
This project evaluates how well large language models can generate semantically correct programs that combine arithmetic logic with graphical rendering. We prompt three LLMs to reconstruct five classic board games in Python using pygame, then automatically test the generated code across three error categories: syntax errors (detected at parse time), semantic errors (missing or incorrect game components), and game logic errors (incorrect win detection, collision handling, or state management).

## My Contributions
- Designed and built the **full automated evaluation pipeline**: syntax validation via `ast.parse` and `py_compile`, semantic checking through dynamic module loading and function signature verification, and game logic testing using headless pygame execution with mock rendering.
- Engineered **headless game logic testing** using AST transformations to strip blocking main loops, mock pygame surfaces, and threaded execution with timeouts — enabling automated testing of interactive graphical programs.
- Wrote **prompt templates** for each game specifying rules, requirements, and expected function interfaces.
- Ran experiments across three models (GPT-4o-mini, Claude 3 Sonnet, Gemini 2.0 Flash) with 20–100 repetitions per game per model at temperature 0.75.
- Analyzed results and identified significant performance gaps between models.

## Games Tested
Each game tests different combinations of state management, spatial reasoning, and rule implementation:

| Game | Key Logic Tested |
|------|-----------------|
| Tic-Tac-Toe | Win detection (rows, columns, diagonals), turn alternation |
| Connect Four | Gravity-based piece dropping, 4-in-a-row detection across axes |
| Snake | Continuous movement, self-collision, growth mechanics |
| Ball Bouncing | Velocity physics, wall collision and reflection |
| Snakes & Ladders | Board traversal, ladder/snake position mapping, dice mechanics |

## Results

**Aggregate pass rates across all five games:**

| Model | N | Syntax | Semantic | Game Logic |
|-------|---|--------|----------|------------|
| GPT-4o-mini | 100 | 99.0% | 57.0% | 57.0% |
| Claude 3 Sonnet | 100 | 100.0% | 60.0% | 60.0% |
| Gemini 2.0 Flash | 500 | 8.4% | 7.4% | 5.4% |

**Per-game breakdown:**

| Game | Model | Syntax | Semantic | Game Logic |
|------|-------|--------|----------|------------|
| Tic-Tac-Toe | GPT-4o-mini | 100% | 0% | 0% |
| | Claude 3 Sonnet | 100% | 0% | 0% |
| | Gemini 2.0 Flash | 9% | 8% | 5% |
| Connect Four | GPT-4o-mini | 100% | 90% | 90% |
| | Claude 3 Sonnet | 100% | 60% | 60% |
| | Gemini 2.0 Flash | 8% | 7% | 6% |
| Snakes & Ladders | GPT-4o-mini | 100% | 55% | 55% |
| | Claude 3 Sonnet | 100% | 90% | 90% |
| | Gemini 2.0 Flash | 8% | 7% | 6% |
| Snake | GPT-4o-mini | 95% | 40% | 40% |
| | Claude 3 Sonnet | 100% | 50% | 50% |
| | Gemini 2.0 Flash | 9% | 7% | 5% |
| Ball Bouncing | GPT-4o-mini | 100% | 100% | 100% |
| | Claude 3 Sonnet | 100% | 100% | 100% |
| | Gemini 2.0 Flash | 8% | 8% | 5% |

## Key Findings

**Syntax correctness does not imply semantic correctness.** GPT-4o-mini and Claude 3 Sonnet achieved near-perfect syntax rates (99–100%) but semantic/logic pass rates varied dramatically by game — from 0% on Tic-Tac-Toe to 100% on Ball Bouncing. This confirms that LLMs can produce syntactically valid code that fails to implement the required game logic.

**Gemini 2.0 Flash struggled significantly with pygame code generation,** achieving only ~8% syntax correctness. The dominant failure modes were `IndentationError` and `SyntaxError: invalid character in identifier`, suggesting the model frequently produces non-ASCII characters or malformed indentation in code blocks.

**Game complexity affects semantic pass rates non-uniformly.** Ball Bouncing (the simplest physics simulation) had 100% pass rates for GPT-4o-mini and Claude, while Tic-Tac-Toe — arguably a simpler game conceptually — had 0% semantic pass rates for both. This is largely attributable to the test framework requiring a specific `check_win(board, player)` function signature that models frequently deviated from, highlighting a limitation of rigid automated semantic testing.

**Semantic pass rates closely tracked game logic pass rates** for GPT-4o-mini and Claude, suggesting that when these models produce structurally correct code (with the expected functions/classes), the underlying logic is usually correct as well.

## Testing Framework Architecture

The evaluation pipeline has three stages:

1. **Syntax validation** — `ast.parse()` and `py_compile.compile()` check for parse-time errors before any execution.
2. **Semantic checking** — The generated code is dynamically loaded as a module, and game-specific checkers verify the presence and basic functionality of required components (e.g., `check_win` for Tic-Tac-Toe, `Snake` class for Snake).
3. **Game logic testing** — AST transformations remove blocking game loops and `if __name__` blocks, pygame is mocked for headless execution, and game functions are called with known inputs to verify correctness (e.g., testing win detection with a board state that should be a win).

## Limitations & Future Work
- **Rigid semantic checking**: The 0% semantic rate on Tic-Tac-Toe for GPT-4o-mini and Claude was caused by the checker requiring a specific `check_win(board, player)` signature. Many implementations used alternative names or signatures. Future work could use more flexible function discovery.
- **Single prompt template**: Each game used one fixed prompt. Prompt variation and few-shot examples could significantly affect results.
- **Model versions**: Results are specific to GPT-4o-mini, Claude 3 Sonnet (2024-02-29), and Gemini 2.0 Flash at the time of testing. Performance may differ with newer model versions.
- **Sample size imbalance**: Gemini was tested with 100 runs per game vs. 20 for OpenAI/Anthropic, which provides more statistical confidence for Gemini results but less for the others.

## Tech Stack
- Python, pygame, numpy
- AST manipulation for safe headless execution
- Dynamic module loading (`importlib`)
- OpenAI, Anthropic, and Google Generative AI APIs
- pytest for framework validation

---

**Link:** [GitHub Repository](https://github.com/Gogo2015/llm-semantic-syntax)
