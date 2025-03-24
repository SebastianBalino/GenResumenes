import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx

gemini_api_key = API_KEY_GEMINI

st.markdown(
    """
    <style>
    .stApp {
        background-color: #1a1a1a; /* Darker blue background */
    }
    .stTitle {
        color: #262730;
        text-align: center;
    }
    .stHeader {
        color: #262730;
    }
    .stWrite {
        color: #262730;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #007bff;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
    }
    .stTextArea>label {
        color: #262730;
    }
    .stTextArea textarea {
        background-color: #f5f5f5; /* Light gray background for text area */
        color: #262730;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')


def summarize_text(text):
    try:
        prompt_brief = f"Eres un experto en análisis de textos. Resume el siguiente texto en 5 frases: {text}"
        prompt_intermediate = f"Eres un experto en análisis de textos. Resume el siguiente texto en 10 frases: {text}"
        prompt_detailed = f"Eres un experto en análisis de textos. Resume el siguiente texto en 30 frases: {text}"
        prompt_keywords = f"Eres un experto en análisis de textos. Extrae las palabras clave más relevantes del siguiente texto: {text}"

        response_brief = model.generate_content(prompt_brief)
        summary_brief = response_brief.text

        response_intermediate = model.generate_content(prompt_intermediate)
        summary_intermediate = response_intermediate.text

        response_detailed = model.generate_content(prompt_detailed)
        summary_detailed = response_detailed.text

        response_keywords = model.generate_content(prompt_keywords)
        keywords = response_keywords.text

        return {
            "brief": summary_brief,
            "intermediate": summary_intermediate,
            "detailed": summary_detailed,
            "keywords": keywords
        }
    except Exception as e:
        return {
            "brief": f"Error al generar el resumen breve: {e}",
            "intermediate": f"Error al generar el resumen intermedio: {e}",
            "detailed": f"Error al generar el resumen detallado: {e}",
            "keywords": f"Error al extraer las palabras clave: {e}"
        }

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_word(word_file):
    doc = docx.Document(word_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

st.header("Resumir Textos")
st.write("Esta aplicación te permite resumir textos de manera rápida y sencilla. Puedes ingresar el texto directamente o subir un archivo PDF o Word.")
st.write("Simplemente sube tu archivo o pega el texto en el área de texto a continuación, y la aplicación generará resúmenes en diferentes longitudes, junto con las palabras clave más relevantes.")

uploaded_file = st.file_uploader("Subir archivo PDF o Word", type=["pdf", "docx"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension == "pdf":
        text_to_summarize = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        text_to_summarize = extract_text_from_word(uploaded_file)
    else:
        st.error("Formato de archivo no soportado. Por favor, suba un archivo PDF o Word.")
        text_to_summarize = ""

    if text_to_summarize:
        st.write("Generando resumen...")
        summaries = summarize_text(text_to_summarize)

        st.subheader("Resumen Breve (5 frases)")
        st.write(summaries["brief"])

        st.subheader("Resumen Intermedio (10 frases)")
        st.write(summaries["intermediate"])

        st.subheader("Resumen Detallado (30 frases)")
        st.write(summaries["detailed"])

        st.subheader("Palabras Clave")
        st.write(summaries["keywords"])