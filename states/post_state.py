import operator
from typing import Annotated, List, TypedDict


class PostSchema(TypedDict):
    prompt: str
    prevPosts: Annotated[List[str], operator.add]
    post: str
    iteration: int
    max_iterations: int
