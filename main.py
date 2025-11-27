import operator
from typing import Annotated, List, Literal, TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate

from models.eval_output import EvalOutputSchema
from states.post_state import PostState
from prompts import generationPrompt, evaluationPrompt, notesPrompt
from chat_models import genModel, evalModelWithStructOutput
from utils.utils import getYoutubeTitle, getOpt, writeToFile, getTranscript
import sys


def generatePost(state: PostState):
    genPrmpt = generationPrompt
    notesPrmpt = notesPrompt
    prevPost = None
    if state["mode"] == 2:
        print(f'Iteration: {state["iteration"]}')

    if "prevPosts" in state and state["prevPosts"]:
        prevPost = state["post"]

    promptStr = ""

    if state["mode"] == 1:
        promptStr = notesPrmpt.format(transcript=state["transcript"])
    elif state["mode"] == 2:
        promptStr = genPrmpt.format(platform=state["platform"], topic=state["topic"])
    print(f"Generating Content")

    op = genModel.invoke(promptStr).content

    if prevPost:
        return {"post": op, "prevPosts": prevPost}
    return {"post": op}


def evaluatePost(state: PostState):
    prompt = evaluationPrompt
    promptStr = prompt.format(platform=state["platform"], post=state["post"])
    print(f"Evaluating Content")
    res = evalModelWithStructOutput.invoke(promptStr)
    print()
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


def checkMode(state: PostState) -> Literal[1, 2]:
    return state["mode"]


# print(evalModel.invoke("Hey, How are you"))

graph = StateGraph(PostState)

graph.add_node("generatePost", generatePost)
graph.add_node("evaluatePost", evaluatePost)

graph.add_edge(START, "generatePost")
graph.add_conditional_edges("generatePost", checkMode, {1: END, 2: "evaluatePost"})
graph.add_conditional_edges(
    "evaluatePost",
    checkPostStatus,
    {
        "approved": END,
        "refused": "generatePost",
    },
)


opt = None
print("--------------------------------------")
print("Please select your requirement.")
print("1. Get Notes from a youtube URL")
print("2. Generate a Post")
print("3. Exit ")
print("--------------------------------------")


def writeToFileAsOp(final_post):
    writeToFile(final_post["post"], final_post["title"])
    print("--------------------------------------")
    print(f"Saved in outputs/{final_post['title']}")
    print("--------------------------------------")


while opt not in [1, 2, 3]:

    opt = input("Please select an option: ")
    print()
    opt = getOpt(opt)

    if opt == 1:
        transcript = None

        while True:
            url = input("Please input youtube URL: ")
            try:
                transcript = getTranscript(url)
                title = getYoutubeTitle(url)
                title = title if len(title) <= 12 else f"{title[:12]}..."
                break
            except:
                print("Video no longer available or Invalid URL. Please try Again")
                continue

        workflow = graph.compile()
        final_post = workflow.invoke(
            PostState(
                **{
                    "platform": "",
                    "iteration": 0,
                    "max_iterations": 0,
                    "topic": "",
                    "title": title,
                    "mode": 1,
                    "transcript": transcript,
                }
            )
        )
        writeToFileAsOp(final_post)

    elif opt == 2:

        platform = None

        print("--------------------------------------")
        print("Please select a platform")
        print("1. LinkedIN")
        print("2. (X) Twitter")
        print("3. Instagram")
        print("--------------------------------------")
        opt = None
        while opt not in [1, 2, 3]:
            opt = input("Select an option: ")
            print()
            platform = None
            opt = getOpt(opt)

            if opt == 1:
                platform = "LINKEDIN"
            if opt == 2:
                platform = "TWITTER (X)"
            if opt == 3:
                platform = "INSTAGRAM"
            else:
                print("Please select an valid option. ")
                continue

        print("--------------------------------------")
        print("Please input your topic for which you want your post to be generated: ")
        print("--------------------------------------")

        topic = input("")
        print()

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
                    "mode": 2,
                    "transcript": "",
                }
            )
        )
        writeToFileAsOp(final_post)
    elif opt == 3:
        print("Exited.\n Thank you.")
    else:
        print("Please select a valid option.\n Select from option 1, 2, 3")
