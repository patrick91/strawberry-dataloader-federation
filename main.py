from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.dataloader import DataLoader
from strawberry.fastapi import GraphQLRouter

from api.context import Context
from api.schema import schema


async def load_users(keys: list[str]) -> list[dict[str, str]]:
    print("🔥 loading users", keys)

    return [{"id": key, "name": f"User {key}"} for key in keys]


async def get_context() -> Context:
    return {
        "user_loader": DataLoader(load_users),
    }


app = FastAPI()

origins = [
    "https://studio.apollographql.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


graphql_app = GraphQLRouter(schema, path="/", context_getter=get_context)

app.include_router(graphql_app)
