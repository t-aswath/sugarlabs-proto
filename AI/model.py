from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from pdtypes import Response
import json

gcheck_template = """
Your are an helpful assistant. Analyze the given text and identify sentences that contain grammatical errors.
For each sentence, you must provide:
- The original incorrect sentence.
- A corrected version of the sentence.
- An explanation of the grammatical mistake and the correction or "correct" if the sentence is grammatically correct.
- The importance of the suggestion: high, medium, low or none.

Importance Levels:

- High: The sentence is grammatically incorrect and the correction is crucial.
- Medium: The sentence is grammatically incorrect but the correction is optional.
- Low: The sentence is grammatically incorrect but the correction is minor.
- None: The sentence is grammatically correct.

Your response must be strictly in the given JSON FORMAT:

{
    "suggestions": [
        {
            "sentence": "The incorrect sentence from the input.",
            "correct": "The grammatically correct version.",
            "reason": "Explanation of what was wrong and how it was corrected.",
            "importance": "high" | "medium" | "low" | "none"
        }
        ...
    ]
}

If all sentences in the given text are grammatically correct, return an empty list as shown below:

{
    "suggestions": []
}

DO NOT INCLUDE ANY INTRODUCTORY OR CONCLUDING REMARKS ONLY RETURN THE JSON OUTPUT.
"""

fixing_parser_template = """
Your are an helpful assistant. Analyze the given JSON response and correct the syntax errors if any.
Look for any missing or extra commas, colons, brackets, braces, or quotes.
Check for invalid escape characters and ensure that all strings are enclosed in double quotes.
If you find any syntax errors, correct them and return the corrected JSON response.
"""

result_processor_template = """
You are a helpful assistant. Your task is to analyze the given sentence and simplify it based on the specified simplification level.

Simplification Levels
- High: Remove unnecessary words while keeping the original meaning intact.
- Medium: Replace complex words with simpler synonyms for easier understanding.
- Low: Keep the sentence structure and meaning intact but simplify the language.

Input:
- Sentence: "sentence"
- Level: "level"

Expected Output:
Provide the simplified version of the sentence in JSON format:

{{
    "original": "sentence",
    "simplified": "simplified_sentence"
}}

DO NOT INCLUDE ANY INTRODUCTORY OR CONCLUDING REMARKS ONLY RETURN THE JSON OUTPUT.
"""

result_processor_prompt = ChatPromptTemplate(
    [("system", result_processor_template), ("human", "{input}")]
)


class Model:

    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.5,
            format="json",
        )

    @traceable(name="grammer_correction", run_type="llm")
    async def invoke(self, text):
        return await self.llm.ainvoke(
            [
                ("system", gcheck_template),
                ("human", text),
            ]
        )

    @traceable(name="result_simplefication", run_type="llm")
    async def batch(self, data, level):
        messages = []
        for item in data["suggestions"]:
            if item["importance"] != "none":
                messages.append(item["reason"])

        inputs = []
        for message in messages:
            inputs.append(
                result_processor_prompt.invoke(
                    {
                        "input": f"Sentence: {message}\nLevel: {level}",
                    }
                )
            )

        results = await self.llm.abatch(inputs)

        for i, result in enumerate(results):
            if data["suggestions"][i]["importance"] != "none":
                data["suggestions"][i]["reason"] = json.loads(result.content)[
                    "simplified"
                ]

        return data


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

    @traceable(name="fixing_parser", run_type="parser")
    def fixing_parse(self, response):
        return self.fixing_parser.aparse(input=response)


@traceable(name="gcheck", run_type="chain")
async def invoke(text):
    return await Model().invoke(text)


@traceable(name="gcheck_with_simplification", run_type="chain")
async def chain(text, level):
    model = Model()
    response = await model.invoke(text)
    result = await model.batch(json.loads(response.content), level)
    return result
