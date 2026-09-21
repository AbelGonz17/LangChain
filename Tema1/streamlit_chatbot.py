import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import PromptTemplate


# Configurar la pagina de la aplicacion
st.set_page_config(page_title = "Chatbot Basico", page_icon = "🤖")
st.title(" 🤖 Chatbot Basico con LangChain")
st.markdown("Este es un *chatbot basico* construido con LangChain y Streamlit. Puedes interactuar con el modelo de lenguaje y obtener respuestas a tus preguntas.")

with st.sidebar:
    st.header("Configuracion")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])

    #Recrear el modelo con nuevos parametros 
    chat_model = ChatOpenAI(model= model_name, temperature= temperature)

# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

#crear el template de prompt con comportamiento especifico
prompt_template = PromptTemplate(
    input_variables=["mensaje","historial"],
    template="""Eres un asistente util y amigable llamado ChatBot Pro.
    
    Historial de conversacion: 
    {historial}

    Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)

#crear cadena usando LCEL (LangChain Expression Language)
cadena = prompt_template | chat_model

# Mostrar mensajes previos en la interfaz
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        #no muestro el mensaje por pantalla
        continue

    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

if st.button("Limpiar Conversacion"):
    st.session_state.mensajes = []
    st.rerun()

#cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")

if pregunta:
    # Mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Generar y mostrar respuesta del asistente
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            #streaming de la respuesta
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))

    except Exception as e:
        st.error(f"Error al generar la respuesta: {str(e)}")
        st.info("Verifica que tu api key de OpenAI este configurada correctamente")
