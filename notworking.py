from dotenv import load_dotenv
import streamlit as st 
import os  
import google.generativeai as genai   
from PIL import Image 

# Load environment variables
load_dotenv()

# Configure the Gemini API with the correct environment variable
api_key = os.getenv("GOOGLE_GENAI_API_KEY")


genai.configure(api_key=api_key)

def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Ensure image is in the correct format
    response = model.generate_content([input_text, image, prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Corrected key
                "data": bytes_data 
            }
        ]
        return image_parts 
    else:
        raise FileNotFoundError("No file uploaded") 

# Default input prompt for calorie calculation


# Streamlit app layout
st.set_page_config(page_title="AI Nutritionist App")
st.header("AI Nutritionist App")

# Text input for custom prompt
input_prompt = st.text_input("Input Prompt: ",key="input")

# File uploader for image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image_display = ""

# Display uploaded image
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    except Exception as e:
        st.error(f"Error opening image: {e}")

# Button for submitting the request
submit = st.button("Tell me the total calories")


input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


"""

# If submit button is clicked
if submit:
    if uploaded_file is None:
        st.error("Please upload an image before submitting.")
    else:
        image_data = input_image_setup(uploaded_file)
        # Assuming the API expects image data as a single dictionary, not a list
        image_part = image_data[0]
        response = get_gemini_response(input_prompt, image_part, input_prompt)
        st.subheader("The Response is:")
        st.write(response)
