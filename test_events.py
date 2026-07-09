import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.agent import attrisense_orchestrator

async def main():
    print("Testing iterating over events from run_async...")
    try:
        final_text = ""
        # Iterate over the async generator
        async for event in attrisense_orchestrator.run_async("analyze EMP0001"):
            print("Event type:", type(event))
            # In ADK, events have a print/represent string or attributes
            # Let's inspect the event attributes
            print("Event dir:", [attr for attr in dir(event) if not attr.startswith("_")])
            # If it's a token/chunk, collect it
            if hasattr(event, "text") and event.text:
                final_text += event.text
            elif hasattr(event, "content") and hasattr(event.content, "parts"):
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        final_text += part.text
            elif hasattr(event, "delta") and event.delta:
                final_text += event.delta

        print("\n--- FINAL COLLECTED TEXT ---")
        print(final_text)
        print("----------------------------")
    except Exception as e:
        print("Error during iteration:", e)

if __name__ == "__main__":
    asyncio.run(main())
