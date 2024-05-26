import streamlit as st 
import google.generativeai as genai
import os 
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        # print("BYTE_DATA:", byte_data)

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]

        return image_parts
    else:
        return FileNotFoundError("No Image Found")
    

#initializing frontend
st.set_page_config(page_title="Calory App", layout="wide",page_icon='🤸🏽')

st.header("Calory App")

name = st.text_input("You Name", key="Name")
TDEE = st.slider("TDEE", min_value=1500,max_value=3000, value=1500,step=5)
st.markdown('[Click here to your Total Daily Energy Expenditure(TDEE)](https://www.forbes.com/health/nutrition/tdee-calculator/)')
calory_consumed_till_now = st.slider("Calories Consumed till now", min_value=0, max_value=3000, value=0, step=5)

if name and TDEE and calory_consumed_till_now :
    st.write("Hello,", name ,"!" "Your TDEE is", TDEE, "and you have consumed", calory_consumed_till_now, "till now" )
else:
    st.markdown("Please fill you name and TDEE")

food_type = st.selectbox("The food photo you are uploading is a ?", ("Breakfast", "Lunch", "Snacks", "Dinner"),
                         index=None,
                         placeholder="selected food type...")

uploaded_file = st.file_uploader("Choose Image to Upload:", type=['jpg','jpeg','png'])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Analyse my food!")

input_prompt = f"""You are an expert nutritionist and you have a client named { name } where 
that client have Total Daily Energy Expenditure(TDEE) = {TDEE}, which the client is eating for {food_type}
you need to see the food items from the image uploaded by your client and answer the follwoing questions and respond in the following format

1. What are the food items in the photo with the calories count
    1. Item 1 - no of calories (quantity) * (calories per unit)
    2. Item 2 - no of calories (quantity) * (calories per unit)
    ...
    n. Item n - no of calories (quantity) * (calories per unit)

2. Total Calories consumes
    calculate correctly Total Calories Consume using below formula and output Total Calories Consume
    
    Total Calories Consume = Σ(quantity_i * calories_per_unit_i) for all food items i (1 to n)
    .......
      
    Total Calories Consume

3. Total Calories Left
    Compute correctly Total Calories Left and Return Total Calories Left
    Total Calories Left = TDEE - Total Calories Consume - {calory_consumed_till_now}
    Total Calories Left

4. What does each food item contrubute?
    1. Item 1 - Carbohydrates/Protiens/Fats/Fiber (percentage)
    2. Item 2 - Carbohydrates/Protiens/Fats/Fiber (percentage)
    ------
    ------

5. Total Macro and Micro Nutrients in the food consume
    1. Carbohydrates -  Total Percantage of Carbohydrates in the Food Consumed
    2. Protiens -  Total Percantage of Protiens in the Food Consumed
    3. Fats -  Total Percantage of Fats in the Food Consumed
    4. Fiber -  Total Percentage of Fiber in the Food Consumed
    5. Vitamins Percenatge (if any)

"""

if submit:
    if image:
        image_data=input_image_setup(uploaded_file)
        response=get_gemini_response(input_prompt,image_data)
        st.header("The Response is")
        st.write(response)
    else:
        st.error("Please Upload file before submitting")
