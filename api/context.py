from typing import TypedDict

from strawberry.dataloader import DataLoader


class Context(TypedDict):
    user_loader: DataLoader[str, dict[str, str]]
