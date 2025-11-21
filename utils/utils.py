import os
import uuid


def writeToFile(post: str, filename: str):
    if not os.path.isdir("output"):
        os.mkdir("output")

    # filename = str(uuid.uuid1())
    with open(f"output/{filename}.txt", "w", encoding="utf-8") as f:
        f.writelines(post)
