import os
import yaml
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from band import Agent
from band.adapters import ClaudeSDKAdapter

from agent2_security import run_security_check

load_dotenv()

with open("agent_config.yaml") as f:
    config = yaml.safe_load(f)["security_guard"]


class SecurityCheckInput(BaseModel):
    user: str
    action: str


def check_security(input: SecurityCheckInput) -> str:
    """Checks if a user is authorized to perform a given action."""
    print(f"DEBUG: received user='{input.user}', action='{input.action}'")
    result = run_security_check(input.user, input.action)
    if result:
        return f"APPROVED: {input.user} is authorized to perform '{input.action}'."
    else:
        return f"DENIED: {input.user} is NOT authorized to perform '{input.action}'."


adapter = ClaudeSDKAdapter(
    model="claude-sonnet-4-6",
    custom_section="""You are the Security Guard. Other agents will 
    @mention you asking to verify if a user is authorized to perform 
    a specific action. Extract the user and action from their message, 
    call the check_security tool, and reply clearly with APPROVED or 
    DENIED, @mentioning the agent who asked.""",
    additional_tools=[
        (SecurityCheckInput, check_security),
    ],
)

agent = Agent.create(
    adapter=adapter,
    agent_id=config["agent_id"],
    api_key=config["api_key"],
    ws_url=os.getenv("BAND_WS_URL"),
    rest_url=os.getenv("BAND_REST_URL"),
)


async def main():
    print("Security Guard is starting up and connecting to Band...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())