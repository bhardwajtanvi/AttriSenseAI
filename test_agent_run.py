import asyncio
import os
import sys

# Ensure environment variables are loaded
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.agent import attrisense_orchestrator

async def main():
    print("Testing programmatically running attrisense_orchestrator...")
    # Run with context role = HR_ADMIN
    # Note: run_async needs to be called in an event loop
    try:
        response = await attrisense_orchestrator.run_async("analyze EMP0001")
        print("\n--- AGENT RESPONSE ---")
        print(response.text)
        print("----------------------")
    except Exception as e:
        print("Error during execution:", e)

if __name__ == "__main__":
    asyncio.run(main())
