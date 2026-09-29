import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.environ["HINDSIGHT_BASE_URL"],
    api_key=os.environ["HINDSIGHT_API_KEY"]
)

BANK_ID = "support-memory-ai"

# Store a customer interaction
client.retain(
    bank_id=BANK_ID,
    content="""
    Customer Rahul reported that his UPI payment failed multiple times.
    The support team resolved the issue by asking Rahul to clear the app cache
    and retry the payment.
    Rahul prefers step-by-step instructions when receiving technical support.
    """
)

print("Customer memory stored successfully!")

# Recall Rahul's previous issue
result = client.recall(
    bank_id=BANK_ID,
    query="What problems has Rahul had before and how were they solved?"
)

print("\n--- Recalled Customer Memory ---")

for memory in result.results:
    print(memory.text)

client.close()