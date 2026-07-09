import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent

def main():
    print("Testing programmatic execution of the agent via Runner...")
    try:
        session_service = InMemorySessionService()
        session = session_service.create_session_sync(user_id="dashboard_user", app_name="attrisense")
        runner = Runner(agent=root_agent, session_service=session_service, app_name="attrisense")

        message = types.Content(
            role="user", parts=[types.Part.from_text(text="analyze EMP0001")]
        )

        print("Executing runner...")
        events = list(
            runner.run(
                new_message=message,
                user_id="dashboard_user",
                session_id=session.id,
                run_config=RunConfig(streaming_mode=StreamingMode.NONE), # Get full response directly
            )
        )

        print(f"\nGot {len(events)} events.")
        
        final_text = ""
        for event in events:
            # Check event types and extract content
            print("Event type:", type(event))
            if hasattr(event, "content") and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        final_text += part.text

        print("\n--- FINAL AGENT REPORT ---")
        print(final_text)
        print("--------------------------")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
