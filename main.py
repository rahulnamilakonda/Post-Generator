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

load_dotenv()


def generatePost(state: PostState):
    prompt = generationPrompt
    promptStr = prompt.format(platform=state["platform"], topic=state["topic"])
    post = genModel.invoke(promptStr).content
    return {"post": post}


def evaluatePost(state: PostState):
    prompt = evaluationPrompt
    promptStr = prompt.format(platform=state["platform"], topic=state["post"])
    res = evalModelWithStructOutput.invoke(promptStr)
    return {"status": res.status, "feedback": [res.feedback]}  # type: ignore


def checkPostStatus(state: PostState) -> Literal["approved", "refused"]:
    if state["status"] == "approved" or state["iteration"] > state["max_iterations"]:
        return "approved"
    else:
        state["iteration"] = 1 + state.get("iteration", 0)
        return "refused"


# print(evalModel.invoke("Hey, How are you"))

graph = StateGraph(PostState)

graph.add_node("generatePost", generatePost)
graph.add_node("evaluatePost", evaluatePost)

graph.add_edge(START, "generatePost")
graph.add_edge("generatePost", "evaluatePost")
graph.add_conditional_edges("evaluatePost", checkPostStatus)
graph.add_edge("approved", END)
graph.add_edge("refused", "generatePost")


workflow = graph.compile()
final_post = workflow.invoke(
    PostState(
        **{
            "platform": "LinkedIn",
            "iteration": 0,
            "max_iterations": 5,
            "topic": "Difference between langchain, langgraph and langsmith",
        }
    )
)
