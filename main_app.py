import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2
from streamlit_autorefresh import st_autorefresh

# load environment variables from .env file
load_dotenv()

# get the connection data from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# establish a database connection
@st.cache_resource
def connect_to_database():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    return conn

# Set the app title
st.title("My Grocery Shopping List")

# Create input fields for users to add items to the list
item = st.text_input("Add an item to your shopping list:")
quantity = st.number_input("Quantity:", min_value=1, max_value=100, value=1)
grocery_shop = st.selectbox("Shop:", ("Ametller", "Bonpreu", "Mercadona", "La Sirena"))

conn = connect_to_database()

# create a cursor object
cur = conn.cursor()

# add item and quantity to the database
if st.button('Add Item'):
    cur.execute("INSERT INTO grocery_list_items (item, quantity, shop) VALUES (%s, %s, %s)", (item, quantity, grocery_shop))
    conn.commit()
    st.write(f"{quantity} {item}(s) added to the grocery list.")

# display the current shopping list
st.subheader("Shopping List")

# execute a SELECT SQL statement to retrieve grocery list items
cur.execute("SELECT * FROM grocery_list_items")

# fetch all rows from the result set
rows = cur.fetchall()

# create a pandas dataframe from the result set
df = pd.DataFrame(rows, columns=['item', 'quantity', 'shop'])

# display the grocery list items in a dataframe
if len(df) > 0:
    st.write("Grocery List Items:")
    st.table(df)

    st.subheader("Remove items")

    item_remove = st.selectbox(
        label="item_remove", options=df["item"].unique().tolist()
    )
    quantity_remove = st.selectbox(
        label="quantity_remove", options=df[df["item"] == item_remove]["quantity"],
    )
    grocery_shop_remove = st.selectbox(
        label="grocery_shop_remove", options=df[df["item"] == item_remove]["shop"],
    )

    # add item and quantity to the database
    if st.button('Remove Item'):
        cur.execute(
            "DELETE FROM grocery_list_items WHERE item = %s AND quantity = %s AND shop = %s",
            (item_remove, quantity_remove, grocery_shop_remove,))
        conn.commit()
        st.write(f"{quantity} {item}(s) removed to the grocery list.")
        st_autorefresh(interval=1, key="refresh_grocery_list")

else:
    st.write("No items in grocery list.")

# # close the cursor and the connection
# cur.close()
# conn.close()