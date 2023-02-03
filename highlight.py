import streamlit as st
import pandas as pd
from IPython.display import display, Markdown, Latex, HTML
st.set_page_config(page_title="Highlight Canadian EPU related words",
                   page_icon=":globe_with_meridians:",
                   layout="wide")

st.title("Highlight Canadian economic policy uncertainty index (EPU) related words")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['body_text'].isnull().sum()
    df.dropna(subset=['body_text'], inplace=True)
    list_exist = []
    selected_words=["economy", "uncertain", "policy", "depression","inflation", "covid19","virus"," bank"]
    for index, row in df.iterrows():
        word = selected_words[0]
        i = 0
        while (word not in row['body_text'] and i < 7 ):
            i +=1
            word = selected_words[i]
        if i<7:
            list_exist.append(selected_words[i])
        else:
            list_exist.append("not_exist") 

    df["existing"]=list_exist
    
    def highlight_selected_text(row):
        text = row["body_text"]
        ext = row["existing"]
        color = {
            "economy": "red",
            "uncertain": "red",
            "policy": "red",
            "depression": "red",
            "inflation": "red",
            "covid19": "red",
            "virus" : "red",
            "bank": "red",
            "not_exist": "black"
        } 
    
        for k, v in color.items():
            text = text.replace(k, f'<span style="color: {v}; font-weight: bold">{k}</span>')
    
        return text
    
    a = df[(df.existing == 'not_exist')].index
    df2 = df.drop(a)
    df2["highlighted"] = df2.apply(highlight_selected_text, axis=1)

    st.write("Highlighted body text and date")
    st.write(HTML(df2[["date", "highlighted"]].head(300).to_html(escape=False)))
