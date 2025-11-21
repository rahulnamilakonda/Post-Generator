from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from models.eval_output import EvalOutputSchema

# models -> https://ai.google.dev/gemini-api/docs/models
load_dotenv()

genModel = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.9)

evalModel = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2)
evalModelWithStructOutput = evalModel.with_structured_output(schema=EvalOutputSchema)
