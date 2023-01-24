from __future__ import annotations


import strawberry

from strawberry.types.info import Info
from .context import Context


@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    name: str

    @classmethod
    async def resolve_reference(
        cls, id: strawberry.ID, info: Info[Context, None]
    ) -> User | None:
        user = await info.context["user_loader"].load(id)

        if user is None:
            return None

        return cls(
            id=user["id"],
            name=user["name"],
        )


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID, info: Info[Context, None]) -> User | None:
        user = await info.context["user_loader"].load(id)

        if user is None:
            return None

        return User(
            id=user["id"],
            name=user["name"],
        )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str) -> str:
        return name


schema = strawberry.federation.Schema(
    Query,
    Mutation,
    enable_federation_2=True,
)
