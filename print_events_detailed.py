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
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id="test_user", app_name="test")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="test")

    message = types.Content(
        role="user", parts=[types.Part.from_text(text="analyze EMP0001")]
    )

    events = list(
        runner.run(
            new_message=message,
            user_id="test_user",
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.NONE),
        )
    )

    for i, event in enumerate(events):
        print(f"\n=== EVENT {i} ===")
        print("Type:", type(event))
        print("Attributes:", dir(event))
        # print string representation of event
        print("Str:", str(event))
        if hasattr(event, "content") and event.content:
            print("Content:", event.content)
        if hasattr(event, "type") and event.type:
            print("Event Type:", event.type)

if __name__ == "__main__":
    main()
