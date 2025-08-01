# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f" :cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie.
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"),col("search_on"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be :', name_on_order)
ingredients_list = st.multiselect('Choose upto 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
 st.write(ingredients_list)
 st.text(ingredients_list)
 ingredients_string = ''
 

 for fruit_chosen in ingredients_list:
      ingredients_string += fruit_chosen + ' '
      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

      st.subheader(fruit_chosen+ ' Nutrition Information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
      sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
   
 st.write(ingredients_string)



my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
time_to_insert = st.button('Submit Order')

if time_to_insert:
  session.sql(my_insert_stmt).collect()
  st.success('Your Smoothie is ordered!', icon="✅")
