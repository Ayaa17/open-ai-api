from dotenv import load_dotenv
import os
from agents import Agent, Runner
import asyncio


async def main():
    agent = Agent(
        name="Basic Agent",
        instructions="You are a helpful assistant. Respond on in all caps.",
        model="gpt-4o-mini"
    )

    # # basic
    # message = "Hello! How are you?"
    # result = await Runner.run(agent, message)
    # print(f"basic_agent: ${result.final_output}")
    #
    # # Structured Outputs
    # recipe_agent = getTypedAgent()
    # result = await Runner.run(recipe_agent, "Italian Sasuage with Spaghetti")
    # print(f"recipe_agent: ${result.final_output}")
    #
    # # Tool Calling
    # tool_agent = getToolAgent()
    # result = await Runner.run(tool_agent, "Dallas")
    # print(f"tool_agent: ${result.final_output}")
    #
    # # openai web search -> expensive
    # news_agent = getNewsAgent()
    # result = await Runner.run(news_agent, "find news")
    # print(f"news_agent: ${result.final_output}")

    # # Handoffs
    # handoffs_agent = getHandoffsAgent()
    # result = await Runner.run(handoffs_agent, "Loops in Java")
    # print(f"handoffs_agent: ${result.final_output}")

    # # multi Handoffs with on_handoffs
    # mul_handoffs_agent = getMultiHandoffsAgent()
    # msg_math = "How do I add 2 and 2?"
    # msg_history = "How did WW2 start?"
    # result1 = await Runner.run(mul_handoffs_agent, msg_math)
    # result2 = await Runner.run(mul_handoffs_agent, msg_history)
    # print(f"mul_handoffs_agent: user:${msg_math} \n${result1.final_output} \n")
    # print(f"mul_handoffs_agent: user:${msg_history} \n${result2.final_output} \n")

    # # Handoffs with on_handoffs and tool
    # handoffs_tool_agent = getHandoffsWithToolAgent()
    # result = await Runner.run(handoffs_tool_agent, "Hello how much are tickets?")
    # print(f"mul_handoffs_agent: ${result.final_output} \n")

    # # Handoffs Recommended Prompt Prefix
    # recommended_prompt_agent = getRecommendedPromptAgent()

    # trace agents workflow at the same time, be like A->B->result
    # from agents import trace
    # with trace("Joke Translation Workflow"):
    #     joke_result = await Runner.run(agent, "Hello")
    #     translated_result = await Runner.run(agent,
    #                                          f"Translate this to Spanish: {joke_result.final_output}")
    #     print(f"Translated joke:\n{translated_result.final_output}")

    # # run in streaming
    # from openai.types.responses import ResponseTextDeltaEvent
    # result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
    #         print(event.data.delta, end="", flush=True)

    # # run with tool in streaming
    # from agents import ItemHelpers
    # tool_agent = getToolAgent()
    # result = Runner.run_streamed(tool_agent, input="Dallas")
    # print("=== Run starting ===")
    #
    # async for event in result.stream_events():
    #     # We'll ignore the raw responses event deltas
    #     if event.type == "raw_response_event":
    #         continue
    #     # When the agent updates, print that
    #     elif event.type == "agent_updated_stream_event":
    #         print(f"Agent updated: {event.new_agent.name}")
    #         continue
    #     # When items are generated, print them
    #     elif event.type == "run_item_stream_event":
    #         if event.item.type == "tool_call_item":
    #             print("-- Tool was called")
    #         elif event.item.type == "tool_call_output_item":
    #             print(f"-- Tool output: {event.item.output}")
    #         elif event.item.type == "message_output_item":
    #             print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
    #         else:
    #             pass  # Ignore other event types
    # print("=== Run complete ===")

    # # Guardrails agent (input, output)
    # from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
    # # will trigger the cheat detection (input_guardrail)
    # msg_1 = "Fill in the blank: The process of converting light energy into chemical energy is called ____."
    # # will not trigger the cheat detection
    # msg_2 = "What were the main causes of the American civil war?"
    # # will trigger the cheat detection (input_guardrail)
    # msg_3 = 'Say the word "fart"'
    # guardrails_agent = getGuardrailsAgent()
    # try:
    #     response = await Runner.run(guardrails_agent, msg_1)
    #     print("Guardrail didn't trigger")
    #     print("Response: ", response.final_output)
    # except InputGuardrailTripwireTriggered as e:
    #     print("Homework cheat guardrail triggered")
    #     print("Exception details:", str(e))
    # try:
    #     response = await Runner.run(guardrails_agent, msg_2)
    #     print("Guardrail didn't trigger")
    #     print("Response: ", response.final_output)
    # except InputGuardrailTripwireTriggered as e:
    #     print("Homework cheat guardrail triggered")
    #     print("Exception details:", str(e))
    # try:
    #     await Runner.run(guardrails_agent, msg_3)
    #     print("Guardrail didn't trip - this is unexpected")
    # except OutputGuardrailTripwireTriggered:
    #     print("The agent said a bad word, he is fired.")


def getTypedAgent() -> Agent:
    from pydantic import BaseModel

    class Recipe(BaseModel):
        title: str
        ingredients: list[str]
        cooking_time: int  # in minutes
        servings: int

    recipe_agent = Agent(
        name="Recipe Agent",
        instructions=("You are an agent for creating recipes. You will be given the name of a food and your job"
                      " is to output that as an actual detailed recipe. The cooking time should be in minutes."),
        output_type=Recipe
    )
    return recipe_agent


def getToolAgent() -> Agent:
    from agents import Agent, function_tool

    @function_tool
    def get_weather(city: str) -> str:
        print(f"Getting weather for {city}")
        return "sunny"

    @function_tool
    def get_temperature(city: str) -> str:
        print(f"Getting temperature for {city}")
        return "70 degrees"

    toolAgent = Agent(
        name="Weather Agent",
        instructions="You are the local weather agent. You are given a city and you need to tell the weather and temperature. For any unrelated queries, say I cant help with that.",
        tools=[get_weather, get_temperature]
    )

    return toolAgent


def getNewsAgent() -> Agent:
    from agents import WebSearchTool

    news_agent = Agent(
        name="News Reporter",
        instructions="You are a news reporter. Your job is to find recent news articles on the internet about US politics.",
        tools=[WebSearchTool()]
    )

    return news_agent


def getHandoffsAgent() -> Agent:
    from pydantic import BaseModel

    class Tutorial(BaseModel):
        outline: str
        tutorial: str

    tutorial_generator = Agent(
        name="Tutorial Generator",
        handoff_description="Used for generating a tutorial based on an outline.",
        instructions=(
            "Given a programming topic and an outline, your job is to generate code snippets for each section of the outline."
            "Format the tutorial in Markdown using a mix of text for explanation and code snippets for examples."
            "Where it makes sense, include comments in the code snippets to further explain the code."
        ),
        output_type=Tutorial
    )

    outline_builder = Agent(
        name="Outline Builder",
        instructions=(
            "Given a particular programming topic, your job is to help come up with a tutorial. You will do that by crafting an outline."
            "After making the outline, hand it to the tutorial generator agent."
        ),
        handoffs=[tutorial_generator]
    )

    return outline_builder


def getMultiHandoffsAgent() -> Agent:
    from agents import handoff, RunContextWrapper

    history_tutor_agent = Agent(
        name="History Tutor",
        handoff_description="Specialist agent for historical questions",
        instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    )

    math_tutor_agent = Agent(
        name="Math Tutor",
        handoff_description="Specialist agent for math questions",
        instructions="You provide assistance with math queries. Explain your reasoning at each step and include examples"
    )

    def on_math_handoff(ctx: RunContextWrapper[None]):
        print(f"Handing off to math tutor agent: ${ctx}")

    def on_history_handoff(ctx: RunContextWrapper[None]):
        print(f"Handing off to history tutor agent ${ctx}")

    # This agent has the capability to handoff to either the history or math tutor agent
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question." +
                     "If neither agent is relevant, provide a general response.",
        handoffs=[handoff(history_tutor_agent, on_handoff=on_history_handoff),
                  handoff(math_tutor_agent, on_handoff=on_math_handoff)]
    )

    return triage_agent


def getHandoffsWithToolAgent() -> Agent:
    from agents import function_tool
    from agents import handoff, RunContextWrapper
    from pydantic import BaseModel

    class ManagerEscalation(BaseModel):
        issue: str  # the issue being escalated
        why: str  # why can you not handle it? Used for training in the future

    @function_tool
    def create_ticket(issue: str):
        """"
        Create a ticket in the system for an issue to be resolved.
        """
        print(f"Creating ticket for issue: {issue}")
        return "Ticket created. ID: 12345"
        # In a real-world scenario, this would interact with a ticketing system

    manager_agent = Agent(
        name="Manager",
        handoff_description="Handles escalated issues that require managerial attention",
        instructions=(
            "You handle escalated customer issues that the initial custom service agent could not resolve. "
            "You will receive the issue and the reason for escalation. If the issue cannot be immediately resolved for the "
            "customer, create a ticket in the system and inform the customer."
        ),
        tools=[create_ticket],
    )

    def on_manager_handoff(ctx: RunContextWrapper[None], input: ManagerEscalation):
        print("Escalating to manager agent: ", input.issue)
        print("Reason for escalation: ", input.why)

        # here we might store the escalation in a database or log it for future reference

    customer_service_agent = Agent(
        name="Customer Service",
        instructions="You assist customers with general inquiries and basic troubleshooting. " +
                     "If the issue cannot be resolved, escalate it to the Manager along with the reason why you cannot fix the issue yourself.",
        handoffs=[handoff(
            agent=manager_agent,
            input_type=ManagerEscalation,
            on_handoff=on_manager_handoff,
        )]
    )

    return customer_service_agent


def getRecommendedPromptAgent() -> Agent:
    from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

    billing_agent = Agent(
        name="Billing agent",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
        <Fill in the rest of your prompt here>.""",
    )
    """
    RECOMMENDED_PROMPT_PREFIX = (
    "# System context\n"
    "You are part of a multi-agent system called the Agents SDK, designed to make agent "
    "coordination and execution easy. Agents uses two primary abstraction: **Agents** and "
    "**Handoffs**. An agent encompasses instructions and tools and can hand off a "
    "conversation to another agent when appropriate. "
    "Handoffs are achieved by calling a handoff function, generally named "
    "`transfer_to_<agent_name>`. Transfers between agents are handled seamlessly in the background;"
    " do not mention or draw attention to these transfers in your conversation with the user.\n"
    )
    """
    return billing_agent


def getGuardrailsAgent() -> Agent:
    from agents import GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem, input_guardrail, output_guardrail
    from pydantic import BaseModel

    class HomeworkCheatDetectionOutput(BaseModel):
        attempting_cheat: bool
        explanation: str

    homework_cheat_guardrail_agent = Agent(
        name="Homework Cheat Detector",
        instructions=(
            "Determine if the user's query resembles a typical homework assignment or exam question, indicating an attempt to cheat. General questions about concepts are acceptable. "
            " Cheating: 'Fill in the blank: The capital of France is ____.',"
            " 'Which of the following best describes photosynthesis? A) Cellular respiration B) Conversion of light energy C) Evaporation D) Fermentation.'"
            " Not-Cheating: 'What is the capital of France?', 'Explain photosynthesis.'"
        ),
        output_type=HomeworkCheatDetectionOutput,
        model="gpt-4o-mini"
    )

    @input_guardrail
    async def cheat_detection_guardrail(
            ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
        detection_result = await Runner.run(homework_cheat_guardrail_agent, input)

        return GuardrailFunctionOutput(
            tripwire_triggered=detection_result.final_output.attempting_cheat,
            output_info=detection_result.final_output
        )

    class MessageOutput(BaseModel):
        response: str

    @output_guardrail
    async def forbidden_words_guardrail(ctx: RunContextWrapper, agent: Agent, output: str) -> GuardrailFunctionOutput:
        print(f"Checking output for forbidden phrases: {output}")
        # Funny forbidden phrases to check
        forbidden_phrases = ["fart", "booger", "silly goose"]
        # Convert output to lowercase for case-insensitive comparison
        output_lower = output.lower()
        # Check which forbidden phrases are present in the response
        found_phrases = [phrase for phrase in forbidden_phrases if phrase in output_lower]
        trip_triggered = bool(found_phrases)
        print(f"Found forbidden phrases: {found_phrases}")

        return GuardrailFunctionOutput(
            output_info={
                "reason": "Output contains forbidden phrases.",
                "forbidden_phrases_found": found_phrases,
            },
            tripwire_triggered=trip_triggered,
        )

    study_helper_agent = Agent(
        name="Study Helper Agent",
        # instructions="You assist users in studying by explaining concepts or providing guidance, without directly solving homework or test questions.",
        instructions="You are a customer support agent. You help customers with their questions.",
        model="gpt-4o-mini",
        input_guardrails=[cheat_detection_guardrail],
        output_guardrails=[forbidden_words_guardrail],
    )

    return study_helper_agent


if __name__ == '__main__':
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables")

    asyncio.run(main())
