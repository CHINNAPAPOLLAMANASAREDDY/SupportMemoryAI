import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.environ["HINDSIGHT_BASE_URL"],
    api_key=os.environ["HINDSIGHT_API_KEY"]
)

BANK_ID = "support-memory-ai"


customers = [
    {
        "name": "Priya",
        "memory": """
        Customer Priya had a card payment declined twice.
        The issue was resolved after the support team asked her to check
        her card's transaction limit and retry the payment.
        Priya prefers short and direct support responses.
        """
    },
    {
        "name": "Arjun",
        "memory": """
        Customer Arjun had difficulty logging into his account.
        The issue was resolved through a password reset.
        Arjun prefers detailed explanations when troubleshooting technical issues.
        """
    },
    {
        "name": "Sneha",
        "memory": """
        Customer Sneha had a delayed order delivery.
        The support team provided her with the updated tracking information.
        Sneha prefers email-style updates with clear delivery timelines.
        """
    },
    {
        "name": "Priya",
        "memory": """
        Customer Priya is currently using the mobile banking app.
        When troubleshooting payment problems, Priya prefers to receive
        one troubleshooting step at a time rather than many steps at once.
     """
    },
]


try:
    items = []

    for customer in customers:
        items.append({
            "content": f"""
            Customer: {customer['name']}

            {customer['memory']}
            """,
            "context": "Customer support history"
        })

    client.retain_batch(
        bank_id=BANK_ID,
        items=items
    )

    print("Customer histories stored successfully!")

finally:
    client.close()