from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder

plantilla_sistema = SystemMessagePromptTemplate.from_template(
 "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}"
)

plantilla_humano = HumanMessagePromptTemplate.from_template(
    "Mi pregunta sobre {tema} es: {pregunta}"
)

chat_prompt = ChatPromptTemplate.from_messages([
    plantilla_sistema,
    plantilla_humano
])

mensajes = chat_prompt.format_messages(
    rol ="Nutricionista",
    especialidad = "dietas veganas",
    tono = "profesional pero accesible",
    tema = "proteina vegetales",
    pregunta = "Cuales son las mejores fuentes de proteina vegana para un atleta profesional?"

)

for m in mensajes:
    print({m.content})