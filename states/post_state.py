import operator
from typing import Annotated, List, Literal, TypedDict


class PostState(TypedDict):
    topic: str
    platform: Literal["LinkedIn", "X-(Twitter)", "Instagram"]
    prevPosts: Annotated[List[str], operator.add]
    feedback: Annotated[List[str], operator.add]
    post: str
    iteration: int
    status: Literal["approved", "refused"]
    max_iterations: int
