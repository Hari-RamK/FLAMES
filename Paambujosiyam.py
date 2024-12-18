import streamlit as st
from streamlit_extras.let_it_rain import rain 
from flask import Flask
from pymongo import MongoClient


client = MongoClient("mongodb://kafka:KAFKA123test@ac-melappl-shard-00-00.w9koftb.mongodb.net:27017,ac-melappl-shard-00-01.w9koftb.mongodb.net:27017,ac-melappl-shard-00-02.w9koftb.mongodb.net:27017/?replicaSet=atlas-tzu88p-shard-0&ssl=true&authSource=admin")
db = client['Pampujosiyam']
collection = db['secretedata'] 

app = Flask(__name__)

def flames(name1, name2):
    male_split = [*name1]
    female_split = [*name2]

    for item in name1:
        if item in female_split:
            male_split.remove(item)
            female_split.remove(item)

    result = male_split + female_split
    count = len(result)

    F = ['Friend', 'Love', 'Affection', 'Marriage', 'Enemy', 'Sister']
    F_emojis = ['🤝', '❤️', '💞', '💍', '💥', '👯‍♀️']

    index = 0
    while len(F) > 1:
        index = (index + count - 1) % len(F)
        F.pop(index)
        F_emojis.pop(index)

    final_result = F[0]
    final_emoji = F_emojis[0]

    return final_result, final_emoji,count

def show_animation(result):
    if result == 'Friend':
        st.balloons()
    elif result == 'Love':
        rain(
            emoji="❤️‍🔥",
            font_size=54,
            falling_speed=5,
            animation_length="infinite",
        )
    elif result == 'Affection':
        st.snow()

    elif result == 'Marriage':
        rain(
            emoji="😍",
            font_size=54,
            falling_speed=5,
            animation_length="5s",
        )

    elif result == 'Enemy':
        rain(
            emoji="😡",
            font_size=54,
            falling_speed=5,
            animation_length="5s",
        )

    elif result == 'Sister':
        rain(
            emoji="🥺",
            font_size=54,
            falling_speed=5,
            animation_length="5s",
        )
   
def store_data(male_name, female_name, result, count):
    data = {
        "Malename": male_name,
        "Femalename": female_name,
        "Result": result,
        "Love_meter": count
    }
    collection.insert_one(data)
    

st.title("PAAMPU JOSIYAM")

male_name = st.text_input("Enter Male Name 👇", key="Malename")

female_name = st.text_input("Enter Female Name 👇", key="Femalename")

if st.button("MERGE"):
    if male_name and female_name:
        result, emoji,count= flames(male_name.lower(), female_name.lower())
        st.write(f"The result is: **{result}** {emoji}")
        show_animation(result) 
        Love_meter = st.slider("Love Meter",0,20,count)
        if Love_meter < 5:
            st.write("Not Work")
        elif Love_meter ==5:
             st.write("Good")
        elif Love_meter >=6:
             st.write("Strong")

        store_data(male_name, female_name, result, Love_meter)
        
        stored_data = list(collection.find())
    else:
        st.warning("Please enter both names to play the game.")
