from langchain_core.runnables import RunnableLambda

paso1 = RunnableLambda(lambda x: f"Numero {x}")

def dublicar_texto(texto):
    return [texto] * 2

paso2 = RunnableLambda(dublicar_texto)

cadena = paso1 | paso2

resultado = cadena.invoke(43)
print(resultado) 