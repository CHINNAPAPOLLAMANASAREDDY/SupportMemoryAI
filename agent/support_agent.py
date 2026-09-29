import os
import asyncio

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv(override=True)

BANK_ID = "support-memory-ai"


def create_client():
    return Hindsight(
        base_url=os.environ["HINDSIGHT_BASE_URL"],
        api_key=os.environ["HINDSIGHT_API_KEY"],
    )


async def _get_customer_memory(customer_name, message):
    client = create_client()

    try:
        result = await client.arecall(
            bank_id=BANK_ID,
            query=f"""
ONLY use memories about the customer named {customer_name}.

Do not use information about other customers.

What previous problems, successful solutions, unresolved issues,
and communication preferences are known for {customer_name}
that are relevant to this new support request?

New support request:
{message}
""",
        )

        memories = []

        for memory in result.results:
            text = getattr(memory, "text", "")

            if customer_name.lower() in text.lower():
                memories.append(text)

        return memories

    finally:
        await client.aclose()


async def _generate_support_response(customer_name, message):
    client = create_client()

    try:
        response = await client.areflect(
            bank_id=BANK_ID,
            query=f"""
Customer name: {customer_name}

New customer message:
"{message}"

Act as a customer support agent.

Use the customer's previous history and preferences.

If the customer prefers one troubleshooting step at a time,
give ONLY ONE troubleshooting step.

If a previous successful solution is relevant, use it.

Do not invent customer history.

Be helpful, friendly, and personalized.
""",
        )

        return response.text

    finally:
        await client.aclose()


async def _save_customer_interaction(customer_name, message, response):
    client = create_client()

    try:
        await client.aretain(
            bank_id=BANK_ID,
            content=f"""
Customer: {customer_name}

Customer message:
{message}

Support response:
{response}
""",
            context="Customer support conversation",
        )

    finally:
        await client.aclose()


def get_customer_memory(customer_name, message):
    return asyncio.run(
        _get_customer_memory(
            customer_name,
            message,
        )
    )


def generate_support_response(customer_name, message):
    return asyncio.run(
        _generate_support_response(
            customer_name,
            message,
        )
    )


def save_customer_interaction(customer_name, message, response):
    return asyncio.run(
        _save_customer_interaction(
            customer_name,
            message,
            response,
        )
    )