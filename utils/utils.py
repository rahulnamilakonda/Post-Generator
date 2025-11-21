import os
import uuid


class Utils:
    def writeToFile(self, post: str):
        if not os.path.isdir("output"):
            os.mkdir("output")

        filename = str(uuid.uuid1())
        with open(f"output/{filename}", "w") as f:
            f.writelines(post)
