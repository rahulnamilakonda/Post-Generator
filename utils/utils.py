import os
import re
import uuid
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import (
    TextFormatter,
    PrettyPrintFormatter,
    WebVTTFormatter,
    SRTFormatter,
)
from bs4 import BeautifulSoup


def writeToFile(post: str, filename: str):
    if not os.path.isdir("output"):
        os.mkdir("output")

    # filename = str(uuid.uuid1())
    with open(f"output/{filename}.txt", "w+", encoding="utf-8") as f:
        f.writelines(post)


def getTranscript(url: str):

    video_id = url.split("v=")[-1]
    ytt = YouTubeTranscriptApi()
    formatter = TextFormatter()

    transcript = ytt.fetch(
        video_id=video_id, languages=["en"], preserve_formatting=True
    )
    opStr = formatter.format_transcript(transcript)
    return opStr


def getOpt(opt: str):
    try:
        opt = int(opt)  # type: ignore
    except ValueError:
        pass
    return opt


def getYoutubeTitle(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    op = soup.find("meta", property="og:title")["content"]  # type:ignore
    op = op if str(op).strip() else "No Filename"
    return re.sub(r"^[A-Za-z ]+$", "", op)  # type:ignore
