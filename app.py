import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler



st.title("Chat with GPT")
gpt_key = st.sidebar.text_input("Enter your GPT API key", type = "password")

if not gpt_key:
    st.info("First enter GPT key")
    st.stop()

model = ChatOpenAI(model = "gpt-5-nano", api_key = gpt_key)
prompt = "You are a helpful assistant. you can write code and answer user question simply and easily. don't write extra information. give the exact answer based on user question"
agent = create_agent(model = model, system_prompt = prompt)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"assistant","content":"Hi!, I am GPT nano"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


qus = st.chat_input("Ask anything")

if qus:
    st.session_state.messages.append({"role":"user", "content":qus})
    st.chat_message("user").write(qus)


    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        response = agent.invoke(
            {"messages": [{"role": "user", "content": qus}]},
            config={"callbacks": [st_cb]}
        )

        st.session_state.messages.append({"role":"assistant","content":response["messages"][-1].content})
        st.write(response["messages"][-1].content)




