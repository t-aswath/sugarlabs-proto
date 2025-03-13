from operator import itemgetter
from langchain.prompts import ChatPromptTemplate
from ollama import AsyncClient
import asyncio


class Model:

    def __init__(self):
        self.task = None

    async def predict(self, input):
        if self.task and not self.task.done():
            print("[LOG]: Cancelling previous task")
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass

        self.task = asyncio.create_task(self.__call(input))
        return await self.task

    async def __call(self, input):
        try:
            response = await AsyncClient().chat(
                model="llama3.2:3b",
                messages=[
                    {
                        "role": "user",
                        "content": input,
                    },
                ],
            )
            return response.message.content
        except asyncio.CancelledError:
            return None


template = """
Given the following text:
\n ------ \n
{input_text}
\n ------ \n
Identify sentences that are not grammatically correct and provide the correct\
version for each. For every ungrammatical sentence, include an explanation of\
the correction. Provide the output strictly in the following JSON format:
[
    {{
        "sentence": "original sentence",
        "correct": "corrected sentence",
        "reason": "explanation of the correction"
        "start": "START INDEX of the sentence in the input text",
        "end": "END INDEX of the sentence in the input text"
    }},
    ...
]
Only include the JSON output with no additional text, commentary, \
or formatting. If all sentences are correct, return an empty array (i.e. []).
"""


async def invoke(text):
    model = Model()
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"input_text": itemgetter("input_text")}
        | prompt
        | (lambda x: x.to_string())
        | model.predict
    )

    result = await chain.ainvoke({"input_text": text})

    return result
