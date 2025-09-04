import streamlit as st
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="EcoChallenge Ultimate 🌱", page_icon="🌍", layout="wide")

# ----------------------------
# Session State Defaults
# ----------------------------
defaults = {
    "login": False, "username": "", "points": 0, "streak": 0, "last_login": "",
    "daily_done": False, "maze_pos": [0,0], "water_maze_pos":[0,0], 
    "tasks_done": [], "quiz_done": False, "crossword_done": False, "avatar": {}
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------
# User Credentials & Files
# ----------------------------
users = {"student1":"pass123","student2":"eco456","guest":"guest123"}
LEADERBOARD_FILE = "leaderboard.csv"
PROGRESS_FILE = "progress.csv"
TASK_UPLOAD_DIR = "uploads"
os.makedirs(TASK_UPLOAD_DIR, exist_ok=True)

# Ensure CSVs exist
for file_name, cols in [(LEADERBOARD_FILE, ["username","points"]), (PROGRESS_FILE, ["username","points","streak","last_login"])]:
    if not os.path.exists(file_name):
        pd.DataFrame(columns=cols).to_csv(file_name,index=False)

# ----------------------------
# Helper Functions
# ----------------------------
def load_progress(username):
    df = pd.read_csv(PROGRESS_FILE)
    if username in df['username'].values:
        data = df[df['username']==username].iloc[0]
        st.session_state["points"] = int(data["points"])
        st.session_state["streak"] = int(data["streak"])
        st.session_state["last_login"] = data.get("last_login","")
    else:
        df = pd.concat([df, pd.DataFrame([{"username":username,"points":0,"streak":0,"last_login":""}])], ignore_index=True)
        df.to_csv(PROGRESS_FILE,index=False)
        st.session_state["points"] = 0
        st.session_state["streak"] = 0
        st.session_state["last_login"] = ""

def save_progress(username):
    df = pd.read_csv(PROGRESS_FILE)
    if username in df['username'].values:
        df.loc[df['username']==username,"points"] = st.session_state["points"]
        df.loc[df['username']==username,"streak"] = st.session_state["streak"]
        df.loc[df['username']==username,"last_login"] = datetime.today().strftime("%Y-%m-%d")
    df.to_csv(PROGRESS_FILE,index=False)

def update_leaderboard(username):
    df = pd.read_csv(LEADERBOARD_FILE)
    if username in df['username'].values:
        df.loc[df['username']==username,'points'] = st.session_state["points"]
    else:
        df = pd.concat([df,pd.DataFrame({"username":[username],"points":[st.session_state['points']]})], ignore_index=True)
    df.to_csv(LEADERBOARD_FILE,index=False)

# ----------------------------
# Login
# ----------------------------
def login():
    st.title("🌱 EcoChallenge Ultimate Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]==password:
            st.session_state["login"] = True
            st.session_state["username"] = username
            load_progress(username)
            st.success(f"Welcome {username}! 🌿")
        else:
            st.error("Invalid credentials!")

# ----------------------------
# Daily Rotating Eco Fact
# ----------------------------
def daily_rotating_fact():
    facts = [
        "🌍 Recycling one aluminum can saves enough energy to run a TV for 3 hours.",
        "💧 1 liter of water takes 1000 liters to produce in food and products.",
        "🌱 Planting trees reduces carbon dioxide in the atmosphere.",
        "♻️ Plastic can take up to 1000 years to decompose!",
        "🌞 Solar energy is renewable and eco-friendly.",
        "🐝 Bees pollinate 70% of the world's crops.",
        "🌊 Reducing water pollution protects marine life.",
        "🌿 Composting reduces methane emissions from landfills."
    ]
    index = datetime.now().timetuple().tm_yday % len(facts)
    st.info(f"💡 Daily Eco Fact: {facts[index]}")

# ----------------------------
# Motivational Messages
# ----------------------------
def motivational_message():
    messages = [
        "🌟 Keep it up! Every small step counts!",
        "💪 You're making the planet greener!",
        "🌱 Today’s eco action inspires tomorrow!",
        "♻️ Recycling is caring for the Earth!",
        "💧 Every drop saved matters!"
    ]
    st.success(random.choice(messages))

# ----------------------------
# Sound Effects
# ----------------------------
def play_sound(event="success"):
    sounds = {
        "success":"https://www.soundjay.com/button/beep-07.wav",
        "fail":"https://www.soundjay.com/button/beep-10.wav",
        "collect":"https://www.soundjay.com/button/button-3.mp3"
    }
    url = sounds.get(event,"")
    if url:
        st.audio(url, format="audio/wav")

# ----------------------------
# Avatar Selection
# ----------------------------
def select_avatar():
    st.subheader("🎨 Choose Your Avatar")
    avatars = {
        "🌱 Green Sprout":"https://i.ibb.co/9p5XHqC/green-sprout.png",
        "💧 Water Drop":"https://i.ibb.co/2yL1y1P/water-drop.png",
        "♻️ Recycling Hero":"https://i.ibb.co/NYcV2w7/recycling-hero.png",
        "🌞 Sun Buddy":"https://i.ibb.co/TkF0L7k/sun-buddy.png",
        "🐝 Bee Friend":"https://i.ibb.co/mvL1Mkg/bee-friend.png"
    }
    cols = st.columns(len(avatars))
    for i,(name,url) in enumerate(avatars.items()):
        with cols[i]:
            if st.button(name,key=name):
                st.session_state["avatar"] = {"name":name,"url":url}
    if st.session_state["avatar"]:
        st.write(f"Your avatar: **{st.session_state['avatar']['name']}**")
        st.image(st.session_state["avatar"]["url"], width=100)

# ----------------------------
# Roadmap
# ----------------------------
def roadmap():
    select_avatar()
    daily_rotating_fact()
    st.write(f"🔥 Current Streak: {st.session_state['streak']} days")
    st.write(f"🏅 Total Points: {st.session_state['points']}")
    challenges = [
        "💧 Save Water Today","🌱 Plant a Tree","♻️ Recycle 3 Items","🌞 Use Solar Energy",
        "🚶‍♂️ Walk/Bike Instead of Driving","🌿 Compost Organic Waste","🛍️ Avoid Plastic Bags",
        "📚 Read Eco-Friendly Tips","🍃 Reduce Paper Usage","🕯️ Turn Off Unused Lights",
        "🌎 Learn About Biodiversity","🐝 Build a Bee Hotel","🌊 Reduce Water Pollution",
        "🍀 Share Eco Knowledge","🧹 Participate in Clean-Up Drive"
    ]
    st.markdown('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:15px">',unsafe_allow_html=True)
    for chal in challenges:
        if st.button(chal,key=chal):
            st.session_state["points"]+=2
            motivational_message()
            st.balloons()
            update_leaderboard(st.session_state["username"])
            save_progress(st.session_state["username"])
        st.markdown(f'<div style="background:linear-gradient(135deg,#81ecec,#6c5ce7);color:white;padding:15px;border-radius:10px;text-align:center">{chal}</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ----------------------------
# Daily Challenge
# ----------------------------
def daily_challenge():
    today = datetime.today().strftime("%Y-%m-%d")
    if st.session_state["last_login"] != today:
        st.session_state["daily_done"] = False
        st.session_state["last_login"] = today
    if not st.session_state["daily_done"]:
        chal = random.choice(["Turn off lights today!","Use reusable bottles!","Plant a tree!","Recycle 3 items!"])
        st.warning(f"🌟 Daily Challenge: {chal}")
        if st.button("Complete Challenge"):
            st.session_state["points"] += 2 + st.session_state["streak"]
            st.session_state["daily_done"] = True
            play_sound("success")
            motivational_message()
            st.success(f"Challenge done! +{2+st.session_state['streak']} points. Total: {st.session_state['points']}")
            st.balloons()
            update_leaderboard(st.session_state["username"])
            save_progress(st.session_state["username"])

# ----------------------------
# Tasks Page
# ----------------------------
def tasks_page():
    st.subheader("🌱 Complete Eco Tasks")
    tasks = {
        "Plant a Tree 🌳":"Upload a photo while planting a tree",
        "Pack Lunch in Eco-friendly container 🍱":"Upload a photo of your packed lunch",
        "Recycle Plastic ♻️":"Upload a photo of items you recycled"
    }
    for task_name,desc in tasks.items():
        st.markdown(f"### {task_name}")
        st.write(desc)
        uploaded_file = st.file_uploader(f"Upload photo for {task_name}", type=["jpg","png"], key=task_name)
        if uploaded_file is not None and task_name not in st.session_state["tasks_done"]:
            save_path = os.path.join(TASK_UPLOAD_DIR,f"{st.session_state['username']}_{task_name.replace(' ','_')}.png")
            with open(save_path,"wb") as f: f.write(uploaded_file.getbuffer())
            st.session_state["points"]+=3
            play_sound("success")
            motivational_message()
            st.success(f"✅ Task Completed! +3 points")
            st.balloons()
            st.session_state["tasks_done"].append(task_name)
            update_leaderboard(st.session_state["username"])
            save_progress(st.session_state["username"])

# ----------------------------
# Recycling Game
# ----------------------------
def recycling_game():
    st.subheader("♻️ Recycling Challenge")
    actions = ["Recycle Plastic","Compost Organic Waste","Use Reusable Bottle","Burn Trash","Dump Waste"]
    action = st.selectbox("Choose your action",actions)
    if st.button("Submit Action"):
        if action in ["Recycle Plastic","Compost Organic Waste","Use Reusable Bottle"]:
            st.session_state["points"]+=3
            play_sound("success")
            motivational_message()
            st.success("✅ Correct! +3 points")
            st.balloons()
        else:
            play_sound("fail")
            st.error("❌ Incorrect action!")
        update_leaderboard(st.session_state["username"])
        save_progress(st.session_state["username"])

# ----------------------------
# Maze Page
# ----------------------------
def maze_page():
    st.subheader("🌀 Eco Maze Challenge (10x10)")
    size = 10
    maze = np.zeros((size,size))
    for _ in range(25): maze[random.randint(0,size-1),random.randint(0,size-1)] = 1
    eco_items = ["🌳","♻️","🌞","💧"]
    item_positions = []
    while len(item_positions)<5:
        x,y = random.randint(0,size-1), random.randint(0,size-1)
        if maze[x,y]==0 and (x,y)!=(0,0) and (x,y)!=(size-1,size-1):
            maze[x,y]=2
            item_positions.append((x,y))
    pos = st.session_state.get("maze_pos",[0,0])
    st.write("Use buttons to move your avatar!")
    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        if st.button("Up"): 
            if pos[0]>0 and maze[pos[0]-1,pos[1]]!=1: pos[0]-=1
    with col2:
        if st.button("Left"): 
            if pos[1]>0 and maze[pos[0],pos[1]-1]!=1: pos[1]-=1
        if st.button("Right"): 
            if pos[1]<size-1 and maze[pos[0],pos[1]+1]!=1: pos[1]+=1
    with col3:
        if st.button("Down"): 
            if pos[0]<size-1 and maze[pos[0]+1,pos[1]]!=1: pos[0]+=1
    if (pos[0],pos[1]) in item_positions:
        fact = random.choice([
            "🌳 Trees absorb CO2 and produce oxygen!",
            "♻️ Recycling reduces landfill waste!",
            "💧 Conserving water saves energy!",
            "🌞 Solar energy is clean and renewable!"
        ])
        st.session_state["points"]+=2
        play_sound("collect")
        motivational_message()
        st.success(f"Collected an eco-item! +2 points. Fact: {fact}")
        st.balloons()
        item_positions.remove((pos[0],pos[1]))
        maze[pos[0],pos[1]] = 0
    st.session_state["maze_pos"] = pos
    display = np.full((size,size),"⬜")
    display[maze==1]="⬛"
    for (x,y) in item_positions: display[x,y]=eco_items[random.randint(0,len(eco_items)-1)]
    display[pos[0],pos[1]]="🟩"
    st.text("\n".join([" ".join(row) for row in display]))
    if pos == [size-1,size-1]:
        st.session_state["points"]+=5
        play_sound("success")
        motivational_message()
        st.success("🎉 Maze Completed! +5 points")
        st.balloons()
        st.session_state["maze_pos"]=[0,0]

# ----------------------------
# Water Maze Page
# ----------------------------
def water_maze_page():
    st.subheader("💧 Water Maze Challenge (10x10)")
    size = 10
    pos = st.session_state.get("water_maze_pos",[0,0])
    st.write("Collect water drops and eco-items!")
    display = np.full((size,size),"💧")
    item_positions = []
    for _ in range(5):
        x,y=random.randint(0,size-1), random.randint(0,size-1)
        if (x,y)!=(0,0) and (x,y)!=(size-1,size-1):
            display[x,y]="🌱"
            item_positions.append((x,y))
    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        if st.button("Up","w"): pos[0]=max(0,pos[0]-1)
    with col2:
        if st.button("Left","a"): pos[1]=max(0,pos[1]-1)
        if st.button("Right","d"): pos[1]=min(size-1,pos[1]+1)
    with col3:
        if st.button("Down","s"): pos[0]=min(size-1,pos[0]+1)
    if (pos[0],pos[1]) in item_positions:
        fact = random.choice([
            "💧 Saving water preserves life!",
            "🌱 Planting reduces heat & CO2!",
            "♻️ Recycling prevents pollution!",
            "🌞 Using solar energy reduces carbon!"
        ])
        st.session_state["points"]+=2
        play_sound("collect")
        motivational_message()
        st.success(f"Collected an eco-item! +2 points. Fact: {fact}")
        st.balloons()
        item_positions.remove((pos[0],pos[1]))
    display[pos[0],pos[1]]="💦"
    st.session_state["water_maze_pos"]=pos
    st.text("\n".join([" ".join(row) for row in display]))
    if pos==[size-1,size-1]:
        st.session_state["points"]+=5
        play_sound("success")
        motivational_message()
        st.success("🎉 Water Maze Completed! +5 points")
        st.balloons()
        st.session_state["water_maze_pos"]=[0,0]

# ----------------------------
# Quiz Page
# ----------------------------
quiz_questions=[
    {"q":"What is the best way to dispose plastic bottles?","options":["Recycle","Burn","Dump"],"answer":"Recycle"},
    {"q":"Which energy is renewable?","options":["Solar","Coal","Oil"],"answer":"Solar"},
    {"q":"Which activity reduces CO2?","options":["Plant trees","Drive car","Burn trash"],"answer":"Plant trees"}
]
def quiz_page():
    st.subheader("📝 Eco Quiz")
    if not st.session_state["quiz_done"]:
        for i,ques in enumerate(random.sample(quiz_questions,len(quiz_questions))):
            ans = st.radio(ques["q"], ques["options"], key=i)
            if st.button(f"Submit Answer {i}"):
                if ans==ques["answer"]:
                    st.session_state["points"]+=2
                    play_sound("success")
                    motivational_message()
                    st.success("✅ Correct! +2 points")
                else:
                    play_sound("fail")
                    st.error(f"❌ Wrong! Correct answer: {ques['answer']}")
        st.session_state["quiz_done"]=True
        save_progress(st.session_state["username"])

# ----------------------------
# Crossword Page
# ----------------------------
crossword_words = ["RECYCLING","TREES","SOLAR","WATER","EARTH"]
def crossword_page():
    st.subheader("✏️ Eco Crossword")
    if not st.session_state["crossword_done"]:
        correct=0
        for w in crossword_words:
            ans = st.text_input(f"Fill the word starting with {w[0]}...",key=w)
            if st.button(f"Check {w}",key=w+"btn"):
                if ans.upper()==w:
                    st.session_state["points"]+=1
                    play_sound("success")
                    motivational_message()
                    st.success("✅ Correct!")
                    correct+=1
                else:
                    play_sound("fail")
                    st.error(f"❌ Correct word: {w}")
        if correct==len(crossword_words):
            st.session_state["crossword_done"]=True
            st.success("🎉 Crossword Completed!")
            st.balloons()
            save_progress(st.session_state["username"])

# ----------------------------
# Leaderboard
# ----------------------------
def leaderboard_page():
    st.subheader("🏆 Leaderboard")
    df = pd.read_csv(LEADERBOARD_FILE).sort_values("points",ascending=False)
    st.dataframe(df)

# ----------------------------
# Main Navigation
# ----------------------------
def main():
    if not st.session_state["login"]:
        login()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to",[
            "Roadmap","Daily Challenge","Tasks","Maze","Water Maze","Recycling Game","Quiz","Crossword","Leaderboard"
        ])
        daily_rotating_fact()
        if page=="Roadmap": roadmap()
        elif page=="Daily Challenge": daily_challenge()
        elif page=="Tasks": tasks_page()
        elif page=="Maze": maze_page()
        elif page=="Water Maze": water_maze_page()
        elif page=="Recycling Game": recycling_game()
        elif page=="Quiz": quiz_page()
        elif page=="Crossword": crossword_page()
        elif page=="Leaderboard": leaderboard_page()

main()
