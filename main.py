import streamlit as st
from PIL import Image
from core.extract import img_to_text
import core.model as m
from core.dataframe import get_individual_prices
import pandas as pd

st.title("Bill Splitter")

n = st.text_input("Enter the number of people:")
if n.isdigit():
    n = int(n)
else:
    st.error("Please enter a valid number of people.")
    st.stop()

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

@st.cache_data
def process_image(file):
    """Extract data from the uploaded image and process it."""
    text = img_to_text(file)
    df_items = m.items_price(text)
    df_price = m.total_gst(text)
    return df_items, df_price

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    df_items, df_price = process_image(uploaded_file)

    rows = df_items.shape[0]

    if "selections" not in st.session_state:
        st.session_state.selections = [[0] * n for _ in range(rows)]

    def update_checkbox_state(row, col, checked):
        st.session_state.selections[row][col] = int(checked)

    st.write("Select options from the grid and enter your input below:")

    for i in range(rows):
        st.write(f"**{df_items['Items'][i]}**")
        cols = st.columns(n)
        for j in range(n):
            with cols[j]:
                st.checkbox(
                    f"Person {j+1}",
                    key=f"{i}-{j}",
                    value=bool(st.session_state.selections[i][j]),
                    on_change=update_checkbox_state,
                    args=(i, j, not st.session_state.selections[i][j]),
                )

    if st.button("Calculate Individual Prices"):
        mat = st.session_state.selections
        amt = get_individual_prices(mat, df_items, df_price)
        split_mat = []
        for i in range(n):
            total = amt[i].sum()
            split_mat.append([f'Person {i+1}', total])
        split_mat = pd.DataFrame(split_mat, columns=["Person", "Amount"])
        
        st.write("Amount to be paid:")
        st.write(split_mat)

    # st.write("Items and Prices:")
    # st.write(df_items)
    # st.write("Price Breakdown with GST:")
    # st.write(df_price)


