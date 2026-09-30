from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto.")
    sentimiento: str = Field(description="Sentimiento del texto ( positivo, negativo o neutro.)")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

structured_llm = llm.with_structured_output(AnalisisTexto)

texto_prueba = "Me encanto la nueva pelicula de accion, tiene muchos efectos especiales y emocion"

resultado = structured_llm.invoke(f"Analiza el siguiente texto : {texto_prueba}")

print(resultado)