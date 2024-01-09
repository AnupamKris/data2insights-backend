import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyBv6A0mzzKHry7TbT6xInbRjRgu9H8_P5o"

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
