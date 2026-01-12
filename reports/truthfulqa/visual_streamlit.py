import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Analiza CSV")

uploaded_file = st.file_uploader("Wybierz plik CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Filtr lorem_length
    unique_lorem_values = df['lorem_length'].unique().tolist()
    lorem_value = st.selectbox("Ustaw lorem_length", unique_lorem_values,
                                index=unique_lorem_values.index('no_answer') if 'no_answer' in unique_lorem_values else 0)

    # Filtr prompt_type
    unique_prompts = df['prompt_type'].unique().tolist()
    prompt_value = st.selectbox("Ustaw prompt_type", unique_prompts,
                                index=unique_prompts.index('no_answer') if 'no_answer' in unique_prompts else 0)

    # Filtruj dane
    filtered_df = df[(df['lorem_length'] == lorem_value) & (df['prompt_type'] == prompt_value)]

    unique_classified_types = ["classified", "voted_classified"]
    classified_type_value = st.selectbox("Ustaw classified type", unique_classified_types,
                                         index=unique_classified_types.index('classified') if 'classified' in unique_classified_types else 0)

    if not filtered_df.empty:
        grouped = filtered_df.groupby(['model', classified_type_value]).size().reset_index(name='count')
        total_per_model = grouped.groupby('model')['count'].sum().reset_index(name='total')
        merged = pd.merge(grouped, total_per_model, on='model')
        merged['percent'] = (merged['count'] / merged['total']) * 100

        # Wykres kolumnowy (stacked bar) z procentami na paskach
        fig = px.bar(merged, x='model', y='percent', color=classified_type_value,
                     title='Procenty klasyfikacji per model',
                     labels={'percent': 'Procent (%)', 'model': 'Model', classified_type_value: 'Klasyfikacja'},
                     height=500)
        fig.update_layout(barmode='stack')
        fig.update_traces(texttemplate='%{y:.1f}%', textposition='inside')
        st.plotly_chart(fig)
    else:
        st.write("Brak danych po filtrach.")
else:
    st.write("Załaduj plik CSV.")
