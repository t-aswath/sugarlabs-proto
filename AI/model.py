from operator import itemgetter
from langchain.prompts import ChatPromptTemplate
from gradio_client import Client


# Model class
class Model:
    def __init__(self):
        # Random free model from huggingface
        self.client = Client("yuntian-deng/ChatGPT")

    def predict(self, input):
        result = self.client.predict(
            inputs=input,
            top_p=1,
            temperature=0.3,
            chat_counter=0,
            chatbot=[],
            api_name="/predict",
        )
        return result


template = """
Given the following text:
\n ------ \n
{input_text}
\n ------ \n
Pick sentences which is not grammatically correct.
and provide the correct version of the sentence.
in the following format:
[sentence: sentence, correct_sentence: correct_sentence, reason: reason]
if all the sentences are correct, just return "ok" nothing else.
"""


def invoke(text):
    model = Model()
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"input_text": itemgetter("input_text")}
        | prompt
        | (lambda x: x.to_string())
        | model.predict
    )

    result = chain.invoke({"input_text": text})

    return result[0][0][1]


# Sample Output from the Model

"""
[
    [
        [
            "Human:
            Given the following text:

            ------

            She go to the park and play with her friends every evening

            ------

            Pick sentences which are not grammatically correct,
            and provide the correct version of the sentence
            in the following format:

            ------

            sentence: (sentence)
            correct_sentence: (correct_sentence)
            reason: (reason)"
        ],
        "------

        sentence: She go to the park and play with her friends every evening
        correct_sentence: She goes to the park and plays with her friends every evening
        reason: The subject 'She' requires the verb 'go' to be in the third-person singular form, which is 'goes,'
        and 'play' should also be in the third-person singular form, which is 'plays.'

        ------ "
    ]
],
1,
<Response [200]>,
{"interactive": True, "__type__": "update"}
"""
