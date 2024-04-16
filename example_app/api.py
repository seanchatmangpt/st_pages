"""soc REST API."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import coloredlogs
from fastapi import FastAPI, Depends

from dspygen.experiments.convo_ddd.abstract_aggregate.conversation_aggregate import ConversationAggregate
from dspygen.experiments.convo_ddd.abstract_event.user_input_received_event import UserInputReceivedEvent
from dspygen.rdddy.actor_system import ActorSystem


async def get_actor_system():
    global actor_system

    try:
        actor_system
    except NameError:
        actor_system = ActorSystem()

    return actor_system  # Assume actor_system is globally available


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""
    # Startup events:
    # - Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # - Add coloredlogs' colored StreamHandler to the root logger.
    coloredlogs.install()
    await get_actor_system()
    yield
    # Shutdown events.


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root(user_input: str, asys: ActorSystem = Depends(get_actor_system)):
    """Read root."""
    convo_agg: ConversationAggregate = await asys.actor_of(ConversationAggregate)
    msg = await convo_agg.handle_user_input(UserInputReceivedEvent(content=user_input))
    return msg.model_dump()
