import streamlit as st
from openai import OpenAI
import os

# --- CONFIGURACIÓN DE LA PÁGINA Y API KEY ---

st.set_page_config(page_title="Asistente de PR para Marcas", layout="wide", initial_sidebar_state="expanded")

# Configuración de la API Key de OpenAI
# Para despliegue en Streamlit Community Cloud, el código usará los "Secrets".
# Si la app da un error, es porque la API Key no está configurada.
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("🔴 **Error: API Key de OpenAI no configurada.**")
    st.info("""
        Para solucionar esto, sigue estos pasos:
        1. Si estás desplegando en Streamlit Community Cloud, asegúrate de haber añadido tu API Key en 'Settings' > 'Secrets'.
        2. El 'Secret' debe tener este formato: OPENAI_API_KEY = "sk-..."
        3. Si ejecutas la app localmente, necesitas establecer una variable de entorno.
    """)
    st.stop()

# --- FUNCIÓN PARA LLAMAR A GPT-4o ---

def call_gpt4o(prompt_text):
    """Función genérica para llamar a la API de OpenAI."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt_text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error al contactar con la API de OpenAI: {e}")
        return None

# --- INTERFAZ DE USUARIO CON STREAMLIT ---

st.title("🤖 Asistente de PR para Marcas")
st.markdown("Herramientas inteligentes impulsadas por GPT-4o para potenciar tu comunicación.")

# --- BARRA LATERAL DE NAVEGACIÓN ---

st.sidebar.title("🛠️ Herramientas")
tool_selection = st.sidebar.radio(
    "Elige una herramienta:",
    (
        "📝 Redacción de Comunicados de Prensa",
        "📲 Redacción de Pitches (Email/WhatsApp)",
        "🧠 Análisis de Temáticas"
    ),
    key="tool_selection"
)
st.sidebar.markdown("---")
st.sidebar.info("Esta app utiliza GPT-4o. Los resultados son generados por IA y deben ser revisados por un profesional.")


# --- LÓGICA PARA CADA HERRAMIENTA ---

# Herramienta 1: Comunicados de Prensa
if tool_selection == "📝 Redacción de Comunicados de Prensa":
    st.header("📝 Redactor de Comunicados de Prensa")
    st.markdown("Carga o pega información base y genera un comunicado de prensa profesional y listo para enviar.")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("1. Configuración")
        tono = st.selectbox("Elige el tono:", ("Corporativo y formal", "Cercano y entusiasta", "Directo y noticioso", "Innovador y moderno"))
        enfoque_medio = st.selectbox("Enfocado a:", ("Medio generalista", "Medio especializado (ej. tecnología, finanzas)", "Revista de estilo de vida", "Blog de nicho"))
        
        st.subheader("2. Información Base")
        info_source = st.radio("Fuente de la información:", ("Pegar texto", "Subir un documento .txt"), horizontal=True)

        contexto_base = ""
        if info_source == "Pegar texto":
            contexto_base = st.text_area("Pega aquí toda la información relevante (datos, citas, contexto, etc.). Cuanto más detalle, mejor.", height=300, placeholder="Ej: La empresa Acme Corp lanza hoy su nuevo producto 'Photon V2'. Reduce el consumo energético en un 50%...")
        else:
            uploaded_file = st.file_uploader("Sube un archivo .txt con la información", type=['txt'])
            if uploaded_file is not None:
                contexto_base = uploaded_file.read().decode("utf-8")
                st.success("Archivo cargado con éxito.")
    
    with col2:
        st.subheader("3. Resultado Generado")
        if st.button("🚀 Generar Comunicado de Prensa", type="primary"):
            if not contexto_base.strip():
                st.warning("Por favor, proporciona la información base para generar el comunicado.")
            else:
                prompt_comunicado = f"""
                Actúa como un experto en relaciones públicas y comunicación corporativa con más de 20 años de experiencia trabajando con marcas de primer nivel. Tu tarea es redactar un comunicado de prensa profesional, claro, objetivo y bien estructurado.

                **Información Base Proporcionada:**
                {contexto_base}

                **Instrucciones de Tono y Enfoque:**
                - **Tono del comunicado:** {tono}
                - **Medio de destino:** {enfoque_medio}. Adapta el lenguaje, la profundidad técnica y los ángulos de interés a este tipo de medio.

                **Estructura Obligatoria del Comunicado:**
                1.  **TÍTULO:** Atractivo, conciso y que resuma la noticia principal. Menos de 15 palabras.
                2.  **SUBTÍTULO:** Informativo, que aporte un dato clave o contexto adicional.
                3.  **ENTRADILLA (LEAD):** Primer párrafo. Debe responder a las 6 Ws del periodismo (Quién, Qué, Cuándo, Dónde, Por qué y Cómo) de forma clara y directa. No más de 50 palabras.
                4.  **CUERPO DEL COMUNICADO:**
                    - Desarrolla la información en orden de importancia (pirámide invertida).
                    - Usa un lenguaje claro, preciso y libre de sesgos. Evita adjetivos subjetivos o frases editorializadas.
                    - Incluye al menos una cita (quote) de un portavoz relevante. Si no se proporciona en la información base, crea una que sea coherente, potente y apropiada para el tono solicitado.
                    - Inserta 2-3 intertítulos relevantes y optimizados para SEO que organicen el contenido y faciliten la lectura.
                5.  **ACERCA DE [Nombre de la Marca]:** Un párrafo estándar (boilerplate) describiendo la empresa. Si no se proporciona, indica "[INSERTAR BOILERPLATE DE LA EMPRESA AQUÍ]".
                6.  **CONTACTO DE PRENSA:**
                    - Nombre: [Nombre de Contacto]
                    - Cargo: [Cargo]
                    - Email: [Email]
                    - Teléfono: [Teléfono]

                Mantén la veracidad como prioridad absoluta basándote únicamente en la información proporcionada. No hagas suposiciones infundadas. El objetivo final es crear un documento listo para ser enviado a periodistas.
                """
                with st.spinner("Redactando el comunicado... ✍️"):
                    resultado = call_gpt4o(prompt_comunicado)
                    st.markdown(resultado)

# Herramienta 2: Pitches
elif tool_selection == "📲 Redacción de Pitches (Email/WhatsApp)":
    st.header("📲 Redactor de Pitches para Periodistas")
    st.markdown("Crea mensajes de presentación cortos y efectivos para captar la atención de periodistas por email o WhatsApp.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("1. Configuración")
        formato_salida = st.radio("Elige el formato:", ("Email de presentación", "Mensaje de WhatsApp"), horizontal=True)
        tono_pitch = st.selectbox("Elige el tono:", ("Directo y conciso", "Amigable e informal", "Formal y respetuoso"))
        enfoque_pitch = st.selectbox("Enfocado a:", ("Periodista de medio generalista", "Periodista de medio especializado", "Influencer o creador de contenido"))
        
        st.subheader("2. Información a Presentar")
        tema_a_presentar = st.text_area("Describe brevemente el tema o la noticia que quieres presentar:", height=150, placeholder="Ej: Lanzamiento de una nueva app de fitness que usa IA para crear rutinas personalizadas.")

    with col2:
        st.subheader("3. Resultado Generado")
        if st.button(f"🚀 Generar {formato_salida}", type="primary"):
            if not tema_a_presentar.strip():
                st.warning("Por favor, describe el tema a presentar.")
            else:
                prompt_pitch = f"""
                Actúa como un PR estratega muy efectivo. Tu objetivo es captar la atención de un periodista para que se interese en un tema.

                **Tema a presentar:**
                {tema_a_presentar}

                **Instrucciones de Tono y Enfoque:**
                - **Tono:** {tono_pitch}
                - **Medio de destino:** {enfoque_pitch}
                - **Formato de salida:** {formato_salida}

                **Tarea:**
                Redacta un mensaje breve y potente.

                **Si el formato es "Email de presentación":**
                - **Asunto:** Crea 3 opciones de asunto. Cortos, intrigantes y que eviten parecer spam.
                - **Cuerpo del email:**
                    - Saludo personalizado (ej: "Hola [Nombre del periodista],").
                    - Gancho inicial: Una frase que conecte el tema con el área de cobertura del periodista o un tema de actualidad.
                    - Pitch: Explica el tema de forma muy breve (2-3 frases), destacando por qué es noticioso o relevante para su audiencia. Menciona el valor único.
                    - Llamada a la acción clara: Ofrecer más información, el comunicado completo, una entrevista, etc.
                    - Despedida cordial.

                **Si el formato es "Mensaje de WhatsApp":**
                - El mensaje debe ser muy corto, ideal para leerse en segundos.
                - Empieza de forma directa y respetuosa.
                - Presenta la noticia en una sola frase potente.
                - Termina con una pregunta o llamada a la acción simple (ej: "¿Te interesa y te envío más info?", "¿Te parece si te comparto el comunicado?").
                - Usa emojis de forma sutil y profesional solo si el tono "amigable e informal" fue seleccionado.
                """
                with st.spinner(f"Creando tu {formato_salida}... 📨"):
                    resultado = call_gpt4o(prompt_pitch)
                    st.markdown(resultado)

# Herramienta 3: Análisis de Temáticas
elif tool_selection == "🧠 Análisis de Temáticas":
    st.header("🧠 Analizador de Temáticas para PR")
    st.markdown("Introduce un tema complejo y obtén un desglose estratégico: glosario, enfoques noticiosos y medios a los que proponerlo.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("1. Tema a Analizar")
        tema_a_analizar = st.text_area("Introduce la temática que quieres analizar:", height=150, placeholder="Ej: 'El impacto de la IA cuántica en la logística', 'sostenibilidad en la moda rápida', 'el auge de las finanzas descentralizadas (DeFi)'.")

    with col2:
        st.subheader("2. Análisis Estratégico")
        if st.button("🚀 Analizar Tema", type="primary"):
            if not tema_a_analizar.strip():
                st.warning("Por favor, introduce una temática para analizar.")
            else:
                prompt_analisis = f"""
                Actúa como un analista de medios y estratega de comunicación senior. Se te ha proporcionado una temática y tu trabajo es desglosarla para que un profesional de PR pueda entenderla rápidamente y proponerla a periodistas de forma efectiva.

                **Temática a analizar:**
                {tema_a_analizar}

                **Tu análisis debe tener obligatoriamente las siguientes 3 secciones, usando formato Markdown para los títulos y listas:**

                ### 1. Glosario de Términos Clave
                Identifica y define de forma sencilla los 5-7 términos más importantes relacionados con la temática. La definición debe ser clara y concisa, pensada para alguien que no es experto en el campo.

                ### 2. Enfoques Noticiosos Potenciales
                Propón entre 3 y 5 ángulos o enfoques periodísticos distintos para abordar este tema. Para cada enfoque, explica brevemente por qué es interesante y qué tipo de historia se podría contar. Sé creativo y piensa en diferentes tipos de audiencias.
                - **Enfoque 1 (Ej. Impacto Humano):** Explora cómo esta temática afecta la vida diaria de las personas.
                - **Enfoque 2 (Ej. Innovación y Futuro):** Céntrate en el aspecto tecnológico y disruptivo.
                - **Enfoque 3 (Ej. Perspectiva de Negocio):** Analiza las oportunidades de mercado, inversión y el impacto económico.
                - **Enfoque 4 (Ej. Ángulo de Controversia/Ética):** Señala los posibles debates, riesgos o dilemas éticos asociados.

                ### 3. Perfiles de Medios y Periodistas Target
                Sugiere 3 perfiles de medios de comunicación o tipos de periodistas a los que se les podría proponer este tema. Justifica cada sugerencia explicando por qué les interesaría y qué enfoque de los anteriores encajaría mejor con su línea editorial.
                - **Perfil 1:** (Ej: "Periodistas de la sección de Tecnología en diarios generalistas como El País o La Vanguardia. Les interesará el enfoque de 'Innovación y Futuro' y cómo afecta al consumidor final.")
                - **Perfil 2:** (Ej: "Redactores en revistas especializadas del sector [X], como [ejemplo de revista]. Buscarán los detalles técnicos y el 'Impacto de Negocio'.")
                - **Perfil 3:** (Ej: "Productores de podcasts de actualidad o negocios. Se enfocarán en la 'historia humana' o en una entrevista profunda sobre la 'controversia'.")
                """
                with st.spinner("Analizando la temática y buscando ángulos... 🧐"):
                    resultado = call_gpt4o(prompt_analisis)
                    st.markdown(resultado)