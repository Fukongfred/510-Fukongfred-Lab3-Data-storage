import os
from dataclasses import dataclass
import datetime

import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Prompt:
    title: str
    prompt: str
    academic: bool = False
    reading: bool = False
    drawing: bool = False
    translate: bool = False
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

def setup_database():
    con = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS prompts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            prompt TEXT NOT NULL,
            academic BOOLEAN DEFAULT FALSE,
            reading BOOLEAN DEFAULT FALSE,
            drawing BOOLEAN DEFAULT FALSE,
            translate BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    con.commit()
    return con, cur

def prompt_form(prompt=None):
    default = Prompt("", "", False, False, False, False) if prompt is None else prompt
    with st.form(key="prompt_form", clear_on_submit=True):
        title = st.text_input("Title", value=default.title)
        prompt_content = st.text_area("Prompt", height=200, value=default.prompt)
        academic = st.checkbox("Academic", value=default.academic)
        reading = st.checkbox("Reading", value=default.reading)
        drawing = st.checkbox("Drawing", value=default.drawing)
        translate = st.checkbox("Translate", value=default.translate)

        submitted = st.form_submit_button("Submit")
        if submitted:
            if not title or not prompt_content:
                st.error('Please fill in both the title and prompt fields.')
                return
            return Prompt(title, prompt_content, academic, reading, drawing, translate)

def edit_prompt(id, title, prompt, academic, reading, drawing, translate):
    cur.execute(
        "UPDATE prompts SET title = %s, prompt = %s, academic = %s, reading = %s, drawing = %s, translate = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (title, prompt, academic, reading, drawing, translate, id,)
    )
    con.commit()

def display_prompts(cur):
    search_query = st.text_input("Search")
    filter_option = st.radio("Filter by", ["All", "Academic", "Reading", "Drawing", "Translate"])

    filter_query = ""
    if filter_option != "All":
        filter_query = f"AND {filter_option.lower()} = TRUE"

    sql_query = f"SELECT * FROM prompts WHERE (title ILIKE %s OR prompt ILIKE %s) {filter_query} ORDER BY created_at DESC"

    cur.execute(sql_query, ('%' + search_query + '%', '%' + search_query + '%',))

    prompts = cur.fetchall()

    for p in prompts:
        with st.expander(p[1]):
            title = st.text_input(f"Title {p[0]}", value=p[1], key=f"title_{p[0]}")
            prompt_content = st.text_area(f"Prompt {p[0]}", height=200, value=p[2], key=f"prompt_{p[0]}")
            academic = st.checkbox("Academic", value=p[3], key=f"academic_{p[0]}")
            reading = st.checkbox("Reading", value=p[4], key=f"reading_{p[0]}")
            drawing = st.checkbox("Drawing", value=p[5], key=f"drawing_{p[0]}")
            translate = st.checkbox("Translate", value=p[6], key=f"translate_{p[0]}")
            if st.button("Update", key=f"update_{p[0]}"):
                edit_prompt(p[0], title, prompt_content, academic, reading, drawing, translate)
                st.success("Prompt updated successfully!")
                st.rerun()
            if st.button("Delete", key=f"del_{p[0]}"):
                cur.execute("DELETE FROM prompts WHERE id = %s", (p[0],))
                con.commit()
                st.success("Prompt deleted successfully!")
                st.rerun()

if __name__ == "__main__":
    st.title("Promptbase")
    st.subheader("A simple app to store and retrieve prompts")

    con, cur = setup_database()

    new_prompt = prompt_form()
    if new_prompt:
        try:
            cur.execute(
                "INSERT INTO prompts (title, prompt, academic, reading, drawing, translate) VALUES (%s, %s, %s, %s, %s, %s)",
                (new_prompt.title, new_prompt.prompt, new_prompt.academic, new_prompt.reading, new_prompt.drawing, new_prompt.translate)
            )
            con.commit()
            st.success("Prompt added successfully!")
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")

    display_prompts(cur)
    con.close()
