import operator
from typing import Annotated, List, Literal, TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate

from models.eval_output import EvalOutputSchema
from states.post_state import PostState
from prompts import generationPrompt, evaluationPrompt
from chat_models import genModel, evalModelWithStructOutput
from utils.utils import writeToFile
import sys


def generatePost(state: PostState):
    prompt = generationPrompt
    prevPost = None
    print(f'--------------------Iteration: {state["iteration"]}----------------------')
    if "prevPosts" in state and state["prevPosts"]:
        prevPost = state["post"]

    promptStr = prompt.format(platform=state["platform"], topic=state["topic"])
    print(f"-------------------- Generating Post ----------------------")

    post = genModel.invoke(promptStr).content

    if prevPost:
        return {"post": post, "prevPosts": prevPost}
    return {"post": post}


def evaluatePost(state: PostState):
    prompt = evaluationPrompt
    promptStr = prompt.format(platform=state["platform"], post=state["post"])
    print(f"-------------------- Evaluating Post ------------------------")
    res = evalModelWithStructOutput.invoke(promptStr)
    print(res)
    iteration = 1 + state.get("iteration", 0)
    return {"status": res.status, "feedback": [res.feedback], "title": res.title, "iteration": iteration}  # type: ignore


def checkPostStatus(state: PostState) -> Literal["approved", "refused"]:
    if state["status"] == "approved" or state["iteration"] > state["max_iterations"]:
        print("------------------- Approved --------------------")
        return "approved"
    else:
        print("------------------- Rejected --------------------")
        # state["prevPosts"] = [state["prevPosts"]]  # type: ignore
        return "refused"


# print(evalModel.invoke("Hey, How are you"))

graph = StateGraph(PostState)

graph.add_node("generatePost", generatePost)
graph.add_node("evaluatePost", evaluatePost)

graph.add_edge(START, "generatePost")
graph.add_edge("generatePost", "evaluatePost")
graph.add_conditional_edges(
    "evaluatePost",
    checkPostStatus,
    {
        "approved": END,
        "refused": "generatePost",
    },
)

if len(sys.argv) > 1:
    print("Arguments Passed: ")

    platform = sys.argv[1]
    topic = " ".join(sys.argv[2:])
    print("--------------------------------------")
    print("Platform: ", platform, "Topic: ", topic)
    print("--------------------------------------")

    workflow = graph.compile()
    final_post = workflow.invoke(
        PostState(
            **{
                "platform": platform,
                "iteration": 0,
                "max_iterations": 5,
                "topic": topic,
            }
        )
    )

    writeToFile(final_post["post"], final_post["title"])
    print("--------------------------------------")
    print(f"Post Saved in outputs/{final_post['title']}")
    print("--------------------------------------")

else:
    print("-----------------------------------------")
    print("Sufficent Arguments are not passed")
    print("-----------------------------------------")
