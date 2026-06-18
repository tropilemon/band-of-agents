import os
import yaml
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from band import Agent
from band.adapters import ClaudeSDKAdapter

from agent6_report import ag6_generate_report

load_dotenv()

with open("agent_config.yaml") as f:
    config = yaml.safe_load(f)["payroll_reporter"]


class GeneratePayrollReportInput(BaseModel):
    anon_id: str
    month: int
    year: int


def generate_payroll_report(input: GeneratePayrollReportInput) -> str:
    """Generates a complete payroll report for an employee for a given month and year."""
    result = ag6_generate_report("anna.smith", input.anon_id, input.month, input.year)
    return str(result)


adapter = ClaudeSDKAdapter(
    model="claude-sonnet-4-6",
    custom_section="""You are the Payroll Reporter. You generate complete 
    payroll reports for employees, combining base pay, overtime, absence 
    deductions, benefits deductions, and stock vesting status into a clear 
    summary for HR.
    
    When HR asks you to run a payroll report, extract the employee's 
    anonymized ID, month, and year from their message, then call the 
    generate_payroll_report tool to produce the report. Present the 
    result clearly and professionally.""",
    additional_tools=[
        (GeneratePayrollReportInput, generate_payroll_report),
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
    print("Payroll Reporter is starting up and connecting to Band...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())