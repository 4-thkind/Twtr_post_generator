# 🐦 Tweet Forge

An agentic **LangGraph** workflow that writes tweets, roasts them, and rewrites them until they're actually good.

No "as an AI language model" energy allowed.

## How it works

Three LLM personas, one loop:

```
START → generate → evaluate ──approved──→ END
                       │
                 needs_improvement
                       │
                       ↓
                    optimize → evaluate (again)
```

| Node | Role | Job |
|---|---|---|
| `generate` | Viral Creator | Writes the first draft from a topic |
| `evaluate` | Ruthless Editor | Scores it on 7 criteria, returns structured `approved` / `needs_improvement` + feedback |
| `optimize` | Punch-Up Writer | Rewrites the tweet based on that feedback |

The loop keeps spinning until the evaluator approves it — or `max_iteration` is hit, whichever comes first.

## Why the evaluator is strict

The evaluator is instructed to assume **every tweet starts at zero** and has to earn approval. It auto-rejects anything that:
- blows the 280-char limit
- reads like generic motivational advice
- smells like AI wrote it
- uses hashtags, clickbait, or tired internet phrases
- has grammar issues or is just confusing

This is what keeps the loop from rubber-stamping mediocre drafts.

## Setup

```bash
pip install langgraph langchain-groq python-dotenv pydantic
```

Add your Groq key to a `.env` file:

```
GROQ_API_KEY=your_key_here
```

## Usage

```bash
python tweet_forge.py
```

You'll be prompted for a topic, and it'll iterate (up to 5 times by default) until it lands on a tweet worth posting.

```
Enter topic: cold coffee

Final Tweet:
...

Evaluation: approved

Feedback:
...
```

## State shape

```python
class TweetState(TypedDict):
    topic: str
    tweet: str
    evaluation: Literal["approved", "needs_improvement"]
    feedback: str
    iteration: int
    max_iteration: int
    tweet_history: Annotated[list[str], operator.add]   # every draft, kept
    feedback_history: Annotated[list[str], operator.add] # every round of feedback, kept
```

`tweet_history` and `feedback_history` accumulate across iterations (via `operator.add`), so you get a full paper trail of how the tweet evolved if you want to inspect it.

## Model

All three roles currently run on `openai/gpt-oss-120b` via Groq — easy to swap per-node if you want a cheaper/faster model doing evaluation vs. generation.

## Tuning knobs

- `max_iteration` — hard cap on optimize/evaluate loops (default: 5)
- `temperature` — currently 0.7 across the board; lower it on the evaluator if you want harsher, more consistent scoring
- Swap `ChatGroq` for any other LangChain chat model if you want to move off Groq

## Known rough edges

- No retry/error handling around the Groq calls — a rate limit or network blip will just crash the run
- `evaluate_tweet` relies on structured output support; if you swap models, make sure the new one supports `.with_structured_output()`
- Character limit is enforced only via prompt instructions, not code — a model can still ignore it
