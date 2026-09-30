from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def preprocess_text(text):
    """Limpia el texto eliminado espacios extras y limitando longitud"""
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

def generate_summary(text):
    """genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oracion: {text}"
    response = llm.invoke(prompt)
    return response.content

summary_branch = RunnableLambda(generate_summary)

def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve resultado estructurado"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde UNICAMENTE en formato JSON valido:
    {{"Sentimiento": "positivo|negativo|neutro", "razon": "justificacion breve"}}
    
    Texto: {text}"""

    response = llm.invoke(prompt)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en analisis"}

sentiment_branch = RunnableLambda(analyze_sentiment)

def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    s_data = data["sentimiento_data"]
    return {
        "resumen": data["resumen"],
        "sentimiento": s_data.get("sentimiento") or s_data.get("Sentimiento"),
        "razon": s_data.get("razon") or s_data.get("Razon"),
    }

merger = RunnableLambda(merge_results)

parallel_analysis = RunnableParallel({
     "resumen": summary_branch,
     "sentimiento_data": sentiment_branch
})

#Cadena completa
chain = preprocessor | parallel_analysis | merger

reviews_batch = [
    "Excelente producto, muy satisfecho con la compra", 
    "Terrible calidad, no lo recomiendo para nada", 
    "Esta bien, cumple su funcion basica pero nada especial"
]

resultado_batch = chain.batch(reviews_batch)

print(resultado_batch)