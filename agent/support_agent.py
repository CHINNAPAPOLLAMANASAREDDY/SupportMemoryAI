import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.environ["HINDSIGHT_BASE_URL"],
    api_key=os.environ["HINDSIGHT_API_KEY"]
)

BANK_ID = "support-memory-ai"


def get_customer_memory(customer_name, message):
    result = client.recall(
        bank_id=BANK_ID,
        query=f"""
        ONLY use memories about the customer named {customer_name}.

        Do not use information about other customers.

        What previous problems, successful solutions, unresolved issues,
        and communication preferences are known for {customer_name}
        that are relevant to this new support request?

        New support request:
        {message}
        """
    )

    customer_memories = []

    for memory in result.results:
        if customer_name.lower() in memory.text.lower():
            customer_memories.append(memory.text)

    return customer_memories


def generate_support_response(customer_name, message):
    response = client.reflect(
        bank_id=BANK_ID,
        query=f"""
        Customer name: {customer_name}

        New customer message:
        "{message}"

        Act as a customer support agent.

        Use relevant information from this customer's previous history.
        Remember previous problems, successful solutions, unresolved issues,
        and communication preferences.

        If a previous solution is relevant, use it.
        If the customer has a communication preference, follow it.

        Do not invent information.
        Be helpful, friendly, and concise.
        """
    )

    return response.text


def save_customer_interaction(customer_name, message, response):
    client.retain(
        bank_id=BANK_ID,
        content=f"""
        Customer: {customer_name}

        Customer message:
        {message}

        Support response:
        {response}
        """,
        context="Customer support conversation"
    )


def main():

    print("================================")
    print("       SUPPORTMEMORY AI")
    print("================================")

    customer_name = input("\nEnter customer name: ")

    message = input("Enter customer message: ")

    print("\nSearching customer memory...")

    memories = get_customer_memory(
        customer_name,
        message
    )

    print("\n=== RELEVANT CUSTOMER MEMORY ===")

    if memories:
        for memory in memories:
            print("-", memory)
    else:
        print("No previous relevant memories found.")

    print("\n=== AI SUPPORT RESPONSE ===")

    response = generate_support_response(
        customer_name,
        message
    )

    print(response)

    save_customer_interaction(
        customer_name,
        message,
        response
    )

    print("\n✓ Interaction saved to Hindsight.")


if __name__ == "__main__":
    try:
        main()
    finally:
        client.close()