from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from pdtypes import Response

gcheck_template = """
Your are an helpful assistant. Analyze the given text and identify sentences that contain grammatical errors.
For each GRAMMATICAL INCORRECT SENTENCE, you must provide:
- The original incorrect sentence.
- A corrected version of the sentence.
- An explanation of the grammatical mistake and the correction.
- The starting and ending index of the incorrect sentence in the input text.

Your response must be strictly in the given JSON FORMAT:

{
    "suggestions": [
        {
            "sentence": "The incorrect sentence from the input.",
            "correct": "The grammatically correct version.",
            "reason": "Explanation of what was wrong and how it was corrected.",
        }
        ...
    ]
}

If all sentences in the given text are grammatically correct, return an empty list as shown below:

{
    "suggestions": []
}

"suggestions" LIST SHOULD ONLY CONTAIN THE GRAMMATICALLY INCORRECT SENTENCES AND THEIR CORRECTIONS.
DO NOT INCLUDE ANY INTRODUCTORY OR CONCLUDING REMARKS ONLY RETURN THE JSON OUTPUT.
"""

fixing_parser_template = """
Your are an helpful assistant. Analyze the given JSON response and correct the syntax errors if any.
Look for any missing or extra commas, colons, brackets, braces, or quotes.
Check for invalid escape characters and ensure that all strings are enclosed in double quotes.
If you find any syntax errors, correct them and return the corrected JSON response.
"""


class Model:

    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.5,
            format="json",
        )

    async def invoke(self, text):
        return await self.llm.ainvoke(
            [
                ("system", gcheck_template),
                ("human", text),
            ]
        )


class Parser:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2:3b")
        self.parser = PydanticOutputParser(pydantic_object=Response)
        self.fixing_parser = OutputFixingParser.from_llm(
            parser=self.parser,
            llm=self.llm,
            prompt=fixing_parser_template,
            max_retries=1,
        )

    def fixing_parse(self, response):
        return self.fixing_parser.aparse(input=response)


async def invoke(text):
    return await Model().invoke(text)


async def fixing_parse(response):
    return Parser().fixing_parse(response)
