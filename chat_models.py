from langchain_google_genai import ChatGoogleGenerativeAI

from models.eval_output import EvalOutputSchema

# models -> https://ai.google.dev/gemini-api/docs/models

genModel = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=1.5)

evalModel = ChatGoogleGenerativeAI(model="gemini-3-pro-preview", temperature=0.2)
evalModelWithStructOutput = evalModel.with_structured_output(EvalOutputSchema)
