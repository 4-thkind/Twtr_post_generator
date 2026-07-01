from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_core.messages import SystemMessage, HumanMessage
import operator

generator_llm = ChatGroq(model='openai/gpt-oss-120b', temperature=0.7)
evaluator_llm = ChatGroq(model='openai/gpt-oss-120b', temperature=0.7)
optimizer_llm = ChatGroq(model='openai/gpt-oss-120b', temperature=0.7)

from pydantic import BaseModel, Field

class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvement"] = Field(..., description="Final evaluation result.")
    feedback: str = Field(..., description="feedback for the tweet.")


structured_evaluator_llm = evaluator_llm.with_structured_output(TweetEvaluation)


class TweetState(TypedDict):

    topic: str
    tweet: str
    evaluation: Literal["approved", "needs_improvement"]
    feedback: str
    iteration: int
    max_iteration: int

    tweet_history: Annotated[list[str], operator.add]
    feedback_history: Annotated[list[str], operator.add]

def generate_tweet(state: TweetState):

    
 messages = [
    SystemMessage(
        content="""
You are one of the best X (Twitter) content creators in the world.

Your posts consistently go viral because they are:
- original
- witty
- emotionally engaging
- highly relatable
- concise
- memorable

Never sound like AI.

Write naturally like an experienced human creator.

Avoid clichés, motivational quotes, and generic advice.

Every post should contain ONE strong idea and end with a satisfying punch.

Never explain the joke.
"""
    ),

    HumanMessage(
        content=f"""
Topic:
{state['topic']}

Requirements:

- Maximum 280 characters
- No hashtags
- No emojis unless they genuinely improve the joke
- No question-answer jokes
- No "Imagine if..."
- No "POV:"
- No clickbait

Write ONE X post that people would want to like, repost, and quote.
"""
    )
]
 

 response = generator_llm.invoke(messages).content

    
 return {'tweet': response, 'tweet_history': [response]}

def evaluate_tweet(state: TweetState):

    
    messages = [
    SystemMessage(
        content="""
You are an elite X (Twitter) content editor.

Your job is NOT to rewrite posts.
Your ONLY job is to evaluate them honestly.

Be extremely critical.

Assume every post starts at a score of 0 and must earn approval.

Evaluate using these criteria:

1. Originality
- Is this a fresh idea?
- Does it avoid clichés?
- Does it sound human?

2. Hook
- Does the first sentence immediately grab attention?

3. Clarity
- Is every sentence easy to understand?
- Is there unnecessary wording?

4. Engagement
- Would people like, repost, or quote this?
- Does it spark curiosity or emotion?

5. Readability
- Is it concise?
- Does it flow naturally?

6. Authenticity
- Does it sound like a real person?
- Does it avoid AI-style writing?

7. Ending
- Does the final line leave an impact?
- Does it avoid weak conclusions?

Automatically reject the post if:
- It exceeds 280 characters.
- It contains generic motivational advice.
- It feels AI-generated.
- It uses unnecessary hashtags.
- It contains obvious clickbait.
- It repeats common internet phrases.
- It has grammar mistakes.
- It is confusing or repetitive.

Approve ONLY if you genuinely believe the post is publish-ready.
"""
    ),

    HumanMessage(
        content=f"""
Evaluate this X post.

Topic:
{state["topic"]}

Post:
{state["tweet"]}

Return ONLY:

evaluation:
approved OR needs_improvement

feedback:
Provide 3-6 specific, actionable suggestions explaining exactly what should be improved.
Do NOT rewrite the post.
"""
    )
]

    response = structured_evaluator_llm.invoke(messages)

    return {'evaluation':response.evaluation, 'feedback': response.feedback, 'feedback_history': [response.feedback]}

def optimize_tweet(state: TweetState):

    messages = [
        SystemMessage(content="You punch up tweets for virality and humor based on given feedback."),
        HumanMessage(content=f"""
Improve the tweet based on this feedback:
"{state['feedback']}"

Topic: "{state['topic']}"
Original Tweet:
{state['tweet']}

Re-write it as a short, viral-worthy tweet. Avoid Q&A style and stay under 280 characters.
""")
    ]

    response = optimizer_llm.invoke(messages).content
    iteration = state['iteration'] + 1

    return {'tweet': response, 'iteration': iteration, 'tweet_history': [response]}

def route_evaluation(state: TweetState):

    if state['evaluation'] == 'approved' or state['iteration'] >= state['max_iteration']:
        return 'approved'
    else:
        return 'needs_improvement'

graph = StateGraph(TweetState)

graph.add_node('generate', generate_tweet)
graph.add_node('evaluate', evaluate_tweet)
graph.add_node('optimize', optimize_tweet)

graph.add_edge(START, 'generate')
graph.add_edge('generate', 'evaluate')

graph.add_conditional_edges('evaluate', route_evaluation, {'approved': END, 'needs_improvement': 'optimize'})
graph.add_edge('optimize', 'evaluate')

workflow = graph.compile()

workflow

if __name__ == "__main__":
    topic=input("Enter topic: ")
    state={"topic":topic,"iteration":1,"max_iteration":5}
    result=workflow.invoke(state)
    print("\nFinal Tweet:\n")
    print(result["tweet"])
    print("\nEvaluation:",result["evaluation"])
    print("\nFeedback:\n",result["feedback"])




