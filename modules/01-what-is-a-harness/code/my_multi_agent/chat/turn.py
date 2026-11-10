"""
"""

from google.adk.runners import Runner
from google.adk.agents import RunConfig
# TODO: import RunConfig

from google.genai import types

from rich.console import Console

from chat.masking import DISPLAY_TEXT_KEY
from chat.render_chat import (
    AnswerStream, View,
    open_answer, append_answer, close_answer,
    print_thinking_header, print_thinking_delta,
    print_tool_call, print_tool_response
)


async def get_async_agent_response(query: str, runner: Runner, run_config: RunConfig, 
                                   user_id, session_id, console: Console, view: View):
    """
    """

    open_kind: str | None = None
    answer: AnswerStream | None = None

    async def close_current(final_text: str | None = None) -> None:
        nonlocal open_kind, answer
        if open_kind == "answer" and answer is not None:
            await close_answer(console, answer, view, final_text)
            answer = None
        elif open_kind == "thinking":
            console.print()
        open_kind = None

    new_msg = types.Content(role = 'user', parts = [types.Part(text=query)])
    
    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, 
                                            new_message=new_msg,
                                            run_config=run_config):
            
            if not event.content or not event.content.parts:
                continue
            
            author = event.author or "agent"
            
            for part in getattr(event.content, 'parts') or []:

                if part.function_call and not event.partial:
                    # tool call
                    # non partial even whose part is a function call.
                    # A tool call ends whatever segment was open: otherwise the tool lines
                    # get drawn above a still-running answer Live and the order scrambles.
                    await close_current()
                    fc = part.function_call
                    print_tool_call(console=console, view=view, author=author, name=fc.name, args=fc.args)
                elif part.function_response:
                    # tool response
                    fr = part.function_response
                    print_tool_response(console=console, view=view, name=fr.name, response=fr.response)
                elif part.text and event.partial:
                    kind = "thinking" if part.thought else "answer"
                    if open_kind != kind:
                        # close previous mode of different kind and potentially open a new answer stream
                        await close_current()
                        if kind == "thinking":
                            # prep for thinking print
                            print_thinking_header(console=console, view=view, author=author)
                        else:
                            # open answer stream
                            answer = open_answer(console=console, view=view, author=author)
                        open_kind = kind
                    if kind == "thinking":
                        # print the actual thinking tokens
                        print_thinking_delta(console=console, view=view, delta = part.text)
                    else:
                        # append to answer stream with this part's text
                        await append_answer(console=console, stream=answer, view=view, delta=part.text)
                elif part.text and not part.thought:
                    # non-partial event not containing thinking tokens: aggregated final message from agent (LLM), authoritative
                    if open_kind != "answer":
                        # close non-answer mode
                        await close_current()
                        answer = open_answer(console=console, view=view, author=author)
                        open_kind = "answer"
                    # add text from final message into stream and close it.
                    # here the open_kind has to be "answer", hence we know which branch of
                    #  close_current() will be chosen.
                    # If the masking callback rewrote this answer for a non-admin, the
                    # name-free version sits in custom_metadata; prefer it. Admin events
                    # never carry the key, so they fall through to the raw text.
                    masked_text: str | None = (event.custom_metadata or {}).get(DISPLAY_TEXT_KEY)
                    await close_current(final_text=masked_text or part.text)
    finally:
        # after turn completion, no stream needed to be open.
        await close_current()
