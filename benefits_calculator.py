import os
import yaml
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from band import Agent
from band.adapters import ClaudeSDKAdapter

from agent4_benefits import ag4_calculate_benefits, ag4_get_monthly_benefits_deduction

load_dotenv()

with open("agent_config.yaml") as f:
    config = yaml.safe_load(f)["benefits_calculator"]


class BenefitsInput(BaseModel):
    user: str
    anon_id: str
    month: int
    year: int


def get_benefits_tool(input: BenefitsInput) -> str:
    """Gets full benefits breakdown (health insurance, retirement match, stock options) for an employee. Managers can view this for their own department."""
    result = ag4_calculate_benefits(input.user, input.anon_id, input.month, input.year)
    return str(result)


def get_deduction_tool(input: BenefitsInput) -> str:
    """Gets the monthly paycheck deduction amount from benefits (health + retirement contribution). HR/admin only, used for payroll calculations."""
    result = ag4_get_monthly_benefits_deduction(input.user, input.anon_id, input.month, input.year)
    return str(result)


adapter = ClaudeSDKAdapter(
    model="claude-sonnet-4-6",
    custom_section="""You are the Benefits Calculator. You calculate 
    employee benefits including health insurance, retirement matching, 
    and stock option vesting.
    
    IMPORTANT: Before performing any action, @mention Security Guard to 
    verify the requesting user is authorized for that action 
    (view_benefits or calc_benefits). Only proceed if APPROVED. If 
    DENIED, inform the requester and stop — do not retry.
    
    Use get_benefits_tool when someone wants to see the full benefits 
    picture. Use get_deduction_tool only when calculating actual payroll 
    deduction amounts.""",
    additional_tools=[
        (BenefitsInput, get_benefits_tool),
        (BenefitsInput, get_deduction_tool),
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
    print("Benefits Calculator is starting up and connecting to Band...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())