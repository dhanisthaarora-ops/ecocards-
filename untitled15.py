# app.py
import streamlit as st
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, date
import streamlit.components.v1 as components

# ----------------------------
# Config & files
# ----------------------------
st.set_page_config(page_title="EcoChallenge Ultimate 🌱", page_icon="🌍", layout="wide")

USERS = {"student1":"pass123","student2":"eco456","guest":"guest123"}
LEADERBOARD_FILE = "leaderboard.csv"
PROGRESS_FILE = "progress.csv"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ensure CSVs exist
if not os.path.exists(LEADERBOARD_FILE):
    pd.DataFrame(columns=["username","points"]).to_csv(LEADERBOARD_FILE,index=False)
if not os.path.exists(PROGRESS_FILE):
    pd.DataFrame(columns=["username","points","streak","last_login","daily_done","tasks_done"]).to_csv(PROGRESS_FILE,index=False)

# ----------------------------
# Session defaults
# ----------------------------
defaults = {
    "login": False, "username": "", "points": 0, "streak": 0, "last_login": "",
    "daily_done": False, "maze_pos": [0,0], "water_maze_pos":[0,0],
    "maze_grid": None, "maze_items": None, "water_maze_items": None,
    "tasks_done": [], "quiz_done": False, "crossword_done": False, "avatar": {},
    "spin_used_date": "", "spin_result": ""
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ----------------------------
# Persistence helpers
# ----------------------------
def ensure_user_row(username):
    df = pd.read_csv(PROGRESS_FILE)
    if username not in df['username'].values:
        new = {"username": username, "points": 0, "streak": 0, "last_login": "", "daily_done": False, "tasks_done": str([])}
        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
        df.to_csv(PROGRESS_FILE, index=False)

def load_progress(username):
    ensure_user_row(username)
    df = pd.read_csv(PROGRESS_FILE)
    row = df[df['username']==username].iloc[0]
    st.session_state["points"] = int(row.get("points",0))
    st.session_state["streak"] = int(row.get("streak",0))
    st.session_state["last_login"] = row.get("last_login","")
    st.session_state["daily_done"] = bool(row.get("daily_done", False))
    tasks = row.get("tasks_done","[]")
    try:
        st.session_state["tasks_done"] = eval(tasks) if isinstance(tasks, str) else tasks
    except:
        st.session_state["tasks_done"] = []

def save_progress(username):
    if username == "":
        return
    ensure_user_row(username)
    df = pd.read_csv(PROGRESS_FILE)
    df.loc[df['username']==username, 'points'] = int(st.session_state["points"])
    df.loc[df['username']==username, 'streak'] = int(st.session_state["streak"])
    df.loc[df['username']==username, 'last_login'] = st.session_state.get("last_login", "")
    df.loc[df['username']==username, 'daily_done'] = bool(st.session_state.get("daily_done", False))
    df.loc[df['username']==username, 'tasks_done'] = str(st.session_state.get("tasks_done", []))
    df.to_csv(PROGRESS_FILE, index=False)
    update_leaderboard(username)

def update_leaderboard(username):
    df = pd.read_csv(LEADERBOARD_FILE)
    if username in df['username'].values:
        df.loc[df['username']==username, 'points'] = int(st.session_state["points"])
    else:
        df = pd.concat([df, pd.DataFrame({"username":[username],"points":[int(st.session_state["points"])]})], ignore_index=True)
    df.to_csv(LEADERBOARD_FILE, index=False)

def get_title(points):
    titles = ["Hero 🌱", "Star ⭐", "Superstar 🌟", "Legend 🌍"]
    level = points // 100
    return titles[level % len(titles)]

# ----------------------------
# Small helpers (UI)
# ----------------------------
def daily_fact():
    facts = [
        "Recycling one aluminum can saves energy to run a TV for ~3 hours.",
        "1 L of water can correspond to ~1000 L in the lifecycle of some foods.",
        "Planting trees helps remove CO2 from air.",
        "Some plastics take ~1000 years to decompose.",
        "Solar energy reduces greenhouse emissions.",
        "Bees pollinate many of our crops.",
        "Composting reduces methane from landfills."
    ]
    idx = date.today().timetuple().tm_yday % len(facts)
    st.info("💡 Daily Eco Fact: " + facts[idx])

def motivational_message():
    msgs = ["🌟 Keep it up!", "💚 Great job!", "♻️ You're making a difference!", "🌱 Amazing work!"]
    st.success(random.choice(msgs))

def play_sound(event="success"):
    sounds = {
        "success":"https://www.soundjay.com/button/beep-07.wav",
        "fail":"https://www.soundjay.com/button/beep-10.wav",
        "collect":"https://www.soundjay.com/button/button-3.mp3"
    }
    url = sounds.get(event,"")
    if url:
        try:
            st.audio(url)
        except:
            pass

# ----------------------------
# Avatar selection
# ----------------------------
def avatar_widget():
    st.subheader("Choose an avatar")
    avatars = {
        "Green Sprout":"https://i.ibb.co/9p5XHqC/green-sprout.png",
        "Water Drop":"https://i.ibb.co/2yL1y1P/water-drop.png",
        "Recycling Hero":"https://i.ibb.co/NYcV2w7/recycling-hero.png",
        "Sun Buddy":"https://i.ibb.co/TkF0L7k/sun-buddy.png",
        "Bee Friend":"https://i.ibb.co/mvL1Mkg/bee-friend.png"
    }
    cols = st.columns(len(avatars))
    for i,(name,url) in enumerate(avatars.items()):
        with cols[i]:
            if st.button(name, key="av_"+name):
                st.session_state["avatar"] = {"name":name,"url":url}
    if st.session_state["avatar"]:
        st.write("Selected:", st.session_state["avatar"]["name"])
        st.image(st.session_state["avatar"]["url"], width=80)

# ----------------------------
# Roadmap page
# ----------------------------
def roadmap_page():
    st.title("🌍 EcoChallenge Ultimate — Roadmap")
    avatar_widget()
    daily_fact()
    st.write(f"**User:** {st.session_state['username']}")
    st.write(f"**Points:** {st.session_state['points']}  •  **Streak:** {st.session_state['streak']}  •  **Rank:** {get_title(st.session_state['points'])}")
    st.markdown("---")
    st.subheader("Quick eco challenges (tap to earn)")
    cards = [
        ("Save Water Today",2),("Plant a Tree",3),("Recycle 3 Items",3),
        ("Use Solar Energy",4),("Walk/Bike Instead of Driving",2),("Compost Organic Waste",3)
    ]
    st.markdown('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">', unsafe_allow_html=True)
    for title,pts in cards:
        if st.button(f"{title} (+{pts})", key="card_"+title):
            st.session_state["points"] += pts
            play_sound("success")
            motivational_message()
            save_progress(st.session_state["username"])
        st.markdown(f'<div style="background:linear-gradient(135deg,#8bd3dd,#6c5ce7);color:#fff;padding:10px;border-radius:8px;text-align:center">{title}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Daily Challenge (photo proof required)
# ----------------------------
def daily_challenge_page():
    st.title("🌟 Daily Challenge (Photo proof required)")
    today = date.today().strftime("%Y-%m-%d")
    # if new day, reset daily_done
    try:
        last = datetime.strptime(st.session_state.get("last_login", ""), "%Y-%m-%d").date()
    except:
        last = None
    if st.session_state.get("last_login","") != today:
        st.session_state["daily_done"] = False
        st.session_state["last_login"] = today
        # simple streak logic
        if last is not None and (date.today() - last).days == 1:
            st.session_state["streak"] += 1
        else:
            st.session_state["streak"] = 1
        save_progress(st.session_state["username"])

    if st.session_state["daily_done"]:
        st.success("✅ You've already completed today's challenge. Come back tomorrow!")
        return

    chal = random.choice(["Turn off lights today!","Use reusable bottles!","Plant a tree!","Recycle 3 items!"])
    st.info(f"Today's Challenge: {chal}")
    uploaded = st.file_uploader("Upload photo proof", type=["png","jpg","jpeg"], key="daily_photo")
    if uploaded is not None:
        fname = f"{st.session_state['username']}_daily_{today}.png"
        with open(os.path.join(UPLOAD_DIR, fname), "wb") as f:
            f.write(uploaded.getbuffer())
        gained = 2 + st.session_state["streak"]
        st.session_state["points"] += gained
        st.session_state["daily_done"] = True
        play_sound("collect")
        motivational_message()
        st.success(f"Daily challenge completed! +{gained} points")
        save_progress(st.session_state["username"])

# ----------------------------
# Tasks (uploads)
# ----------------------------
def tasks_page():
    st.title("📸 Tasks — Upload Proof")
    tasks = {
        "Plant a Tree": "Upload a photo while planting a tree",
        "Pack Eco Lunch": "Upload a photo of your reusable lunch",
        "Recycle Items": "Upload a photo of items you recycled"
    }
    for t,desc in tasks.items():
        st.subheader(t)
        st.write(desc)
        uploaded = st.file_uploader(f"Upload for {t}", type=["png","jpg","jpeg"], key="task_"+t)
        if uploaded is not None and t not in st.session_state["tasks_done"]:
            fname = f"{st.session_state['username']}_{t.replace(' ','_')}.png"
            with open(os.path.join(UPLOAD_DIR, fname), "wb") as f:
                f.write(uploaded.getbuffer())
            st.session_state["points"] += 3
            st.session_state["tasks_done"].append(t)
            play_sound("success")
            motivational_message()
            st.success(f"Task '{t}' completed! +3 points")
            save_progress(st.session_state["username"])

# ----------------------------
# Recycling Game
# ----------------------------
def recycling_game_page():
    st.title("♻️ Recycling Challenge")
    scenario = random.choice([
        ("You find a plastic bottle in the park.", ["Recycle", "Burn", "Dump"]),
        ("You have banana peels after lunch.", ["Recycle", "Compost", "Burn"]),
        ("You find an empty tin can.", ["Recycle", "Trash", "Burn"])
    ])
    st.write(scenario[0])
    choice = st.selectbox("Choose action", scenario[1], key="recycle_choice")
    if st.button("Submit", key="recycle_submit"):
        if choice in ["Recycle","Compost"]:
            st.session_state["points"] += 3
            play_sound("success")
            motivational_message()
            st.success("✅ Good choice! +3 points")
        else:
            play_sound("fail")
            st.error("❌ Not the best choice.")
        save_progress(st.session_state["username"])

# ----------------------------
# Maze (persistent items stored in session_state)
# ----------------------------
def init_maze(size=10):
    if st.session_state.get("maze_grid") is None:
        grid = np.zeros((size,size), dtype=int)
        for _ in range(int(size*size*0.12)):
            x,y = random.randrange(size), random.randrange(size)
            if (x,y) not in [(0,0),(size-1,size-1)]:
                grid[x,y]=1
        items = {}
        emojis = ["🌳","♻️","🌞","💧","🐝"]
        placed = 0
        while placed < 6:
            x,y = random.randrange(size), random.randrange(size)
            key = f"{x}_{y}"
            if grid[x,y]==0 and key not in items and (x,y) not in [(0,0),(size-1,size-1)]:
                items[key] = random.choice(emojis)
                placed += 1
        st.session_state["maze_grid"] = grid.tolist()
        st.session_state["maze_items"] = items

def maze_page():
    st.title("🌀 Eco Maze")
    size=10
    init_maze(size)
    grid = np.array(st.session_state["maze_grid"])
    pos = st.session_state.get("maze_pos",[0,0])
    cols = st.columns([1,1,1])
    with cols[0]:
        if st.button("Up", key="m_up"):
            if pos[0]>0 and grid[pos[0]-1,pos[1]]!=1:
                pos[0]-=1
    with cols[1]:
        if st.button("Left", key="m_left"):
            if pos[1]>0 and grid[pos[0],pos[1]-1]!=1:
                pos[1]-=1
        if st.button("Right", key="m_right"):
            if pos[1]<size-1 and grid[pos[0],pos[1]+1]!=1:
                pos[1]+=1
    with cols[2]:
        if st.button("Down", key="m_down"):
            if pos[0]<size-1 and grid[pos[0]+1,pos[1]]!=1:
                pos[0]+=1

    key = f"{pos[0]}_{pos[1]}"
    if key in st.session_state["maze_items"]:
        emo = st.session_state["maze_items"].pop(key)
        st.session_state["points"] += 2
        play_sound("collect")
        motivational_message()
        st.success(f"Collected {emo}! +2 points")
        save_progress(st.session_state["username"])
    st.session_state["maze_pos"] = pos

    # display
    display = np.full((size,size), "⬜", dtype=object)
    display[grid==1] = "⬛"
    for k,v in st.session_state["maze_items"].items():
        x,y = map(int,k.split("_"))
        display[x,y] = v
    display[pos[0],pos[1]] = "🟩"
    st.text("\n".join([" ".join(row) for row in display.tolist()]))

    if pos == [size-1,size-1]:
        st.session_state["points"] += 6
        play_sound("success")
        st.success("🎉 Maze finished! +6 points")
        st.session_state["maze_pos"] = [0,0]
        save_progress(st.session_state["username"])

# ----------------------------
# Water Maze
# ----------------------------
def init_water_maze(size=10):
    if st.session_state.get("water_maze_items") is None:
        items = {}
        emojis = ["💧","🌱","♻️","🌞"]
        placed = 0
        while placed < 6:
            x,y = random.randrange(size), random.randrange(size)
            key = f"{x}_{y}"
            if key not in items and (x,y) not in [(0,0),(size-1,size-1)]:
                items[key] = random.choice(emojis)
                placed += 1
        st.session_state["water_maze_items"] = items

def water_maze_page():
    st.title("💧 Water Maze")
    size=10
    init_water_maze(size)
    pos = st.session_state.get("water_maze_pos",[0,0])
    c1,c2,c3 = st.columns([1,1,1])
    with c1:
        if st.button("Up", key="w_up"): pos[0]=max(0,pos[0]-1)
    with c2:
        if st.button("Left", key="w_left"): pos[1]=max(0,pos[1]-1)
        if st.button("Right", key="w_right"): pos[1]=min(size-1,pos[1]+1)
    with c3:
        if st.button("Down", key="w_down"): pos[0]=min(size-1,pos[0]+1)

    key = f"{pos[0]}_{pos[1]}"
    if key in st.session_state["water_maze_items"]:
        emo = st.session_state["water_maze_items"].pop(key)
        st.session_state["points"] += 2
        play_sound("collect")
        motivational_message()
        st.success(f"Collected {emo}! +2 points")
        save_progress(st.session_state["username"])
    st.session_state["water_maze_pos"] = pos

    # render
    display = np.full((size,size), "💧", dtype=object)
    for k,v in st.session_state["water_maze_items"].items():
        x,y = map(int,k.split("_"))
        display[x,y] = v
    display[pos[0],pos[1]] = "💦"
    st.text("\n".join([" ".join(row) for row in display.tolist()]))

    if pos == [size-1,size-1]:
        st.session_state["points"] += 6
        play_sound("success")
        st.success("🎉 Water maze finished! +6 points")
        st.session_state["water_maze_pos"] = [0,0]
        save_progress(st.session_state["username"])

# ----------------------------
# Quiz
# ----------------------------
quiz_bank = [
    {"q":"What should you do with a plastic bottle?","options":["Recycle","Burn","Dump"],"answer":"Recycle"},
    {"q":"Which energy source is renewable?","options":["Solar","Coal","Oil"],"answer":"Solar"},
    {"q":"Which helps reduce CO2?","options":["Plant trees","Drive car","Burn trash"],"answer":"Plant trees"},
    {"q":"Which is compostable?","options":["Banana peel","Plastic bag","Aluminum can"],"answer":"Banana peel"},
    {"q":"Which saves water?","options":["Fix leaks","Let taps run","Water lawn at noon"],"answer":"Fix leaks"}
]
def quiz_page():
    st.title("📝 Eco Quiz")
    if not st.session_state["quiz_done"]:
        questions = random.sample(quiz_bank,3)
        gained = 0
        for i,q in enumerate(questions):
            ans = st.radio(q["q"], q["options"], key=f"quiz_{i}")
            if st.button(f"Submit {i}", key=f"quiz_btn_{i}"):
                if ans == q["answer"]:
                    st.session_state["points"] += 2
                    gained += 2
                    play_sound("success")
                    motivational_message()
                    st.success("✅ Correct! +2 points")
                else:
                    play_sound("fail")
                    st.error(f"❌ Wrong. Correct: {q['answer']}")
        st.session_state["quiz_done"] = True
        if gained>0:
            save_progress(st.session_state["username"])
    else:
        st.info("You already attempted the quiz this session.")

# ----------------------------
# Crossword (clue-style updated)
# ----------------------------
CROSSWORD = {
    "SUSTAINABILITY": "Long-term balance of nature and resources",
    "RECYCLE": "You should do this with bottles, cans and paper ♻️",
    "WATER": "Covers 70% of Earth but drinkable part is limited 💧",
    "GREEN": "Color often associated with eco-friendly living 🌱",
    "SOLAR": "Clean energy from the Sun ☀️",
    "TREE": "Provides shade, habitat and oxygen 🌳"
}
def crossword_page():
    st.title("✏️ Eco Crossword (Clues)")
    # show 5 random words each time unless already completed
    if st.session_state.get("crossword_done", False):
        st.success("✅ Crossword already completed!")
        return
    sample = random.sample(list(CROSSWORD.items()), k=5)
    inputs = {}
    for word, clue in sample:
        inputs[word] = st.text_input(f"Clue: {clue}", key="cw_"+word)
    if st.button("Check Crossword"):
        correct = 0
        for word in inputs:
            if inputs[word].strip().upper() == word:
                correct += 1
        if correct == len(inputs):
            st.session_state["points"] += 10
            st.session_state["crossword_done"] = True
            play_sound("success")
            st.success(f"🎉 All correct! +10 points")
            st.balloons()
            save_progress(st.session_state["username"])
        else:
            st.warning(f"You got {correct}/{len(inputs)} correct. Try again!")

# ----------------------------
# Spin-the-wheel (server chooses prize + JS anim)
# ----------------------------
def spin_wheel_page():
    st.title("🎡 Spin-the-Wheel")
    # one spin per day
    today = date.today().strftime("%Y-%m-%d")
    if st.session_state.get("spin_used_date","") == today:
        st.info("You already spun today — come back tomorrow!")
        return

    options = [
        { "label":"+5 Points 🌱", "value":5},
        { "label":"+10 Points 💧", "value":10},
        { "label":"Eco Fact 💡: Recycling 1 ton of paper saves 17 trees!", "value":0},
        { "label":"Challenge 🎯: Plant a tree this week!", "value":0},
        { "label":"Jackpot 🎉 +20 Points!", "value":20},
        { "label":"Try Again 🔄", "value":0}
    ]

    st.write("Press **Spin** below. The wheel animation will run and the server-assigned result will be shown and applied to your points.")

    if st.button("Spin Now"):
        # server picks random index
        idx = random.randrange(len(options))
        prize = options[idx]
        st.session_state["spin_result"] = prize["label"]
        # update points immediately if numeric
        gained = int(prize["value"])
        if gained > 0:
            st.session_state["points"] += gained
        st.session_state["spin_used_date"] = today
        save_progress(st.session_state["username"])
        update_leaderboard(st.session_state["username"])

        # render JS wheel and animate to selected index
        labels = [o["label"] for o in options]
        # compute rotation so that chosen segment lands at top visually
        target_index = idx
        html = f"""
        <!doctype html>
        <html>
        <head>
        <style>
        #wheel{{width:360px;height:360px;border-radius:50%;position:relative;overflow:hidden;margin:0 auto;transform:rotate(0deg);transition:transform 4s cubic-bezier(0.33,1,0.68,1);}}
        .segment{{position:absolute;width:50%;height:50%;transform-origin:100% 100%;clip-path:polygon(0 0,100% 0,100% 100%);}}
        .label{{position:absolute;width:200px;left:50%;top:50%;transform:translate(-50%,-50%);font-size:14px;text-align:center;}}
        #spinbtn{{display:block;margin:15px auto;padding:10px 20px;font-size:18px;}}
        </style>
        </head>
        <body>
        <div id='wheel'></div>
        <button id='spinbtn' onclick='startSpin()'>Spin (Animating...)</button>
        <script>
        const options = {labels};
        const wheel = document.getElementById('wheel');
        const n = options.length;
        // create segments
        for(let i=0;i<n;i++){{
            const seg = document.createElement('div');
            seg.className='segment';
            seg.style.background = i%2==0 ? '#66bb6a' : '#43a047';
            seg.style.transform = 'rotate(' + (360/n * i) + 'deg)';
            seg.style.clipPath = 'polygon(0 0, 100% 0, 100% 100%)';
            seg.innerHTML = '<div class="label" style="transform: rotate(' + (360/n * i + 360/(2*n)) + 'deg)">' + options[i] + '</div>';
            wheel.appendChild(seg);
        }}
        function startSpin(){{
            // rotation to land targetIndex at top (approx)
            const targetIndex = {target_index};
            const extra = 360 * 8; // spins
            const degreesPerSeg = 360 / n;
            // we want segment center to be at -90deg (top), so compute angle
            const targetAngle = extra + (targetIndex * degreesPerSeg) + degreesPerSeg/2;
            wheel.style.transform = 'rotate(' + targetAngle + 'deg)';
            setTimeout(()=>{{ alert('🎉 Result: ' + options[targetIndex]); }}, 4200);
        }}
        // auto-start animation (since Python just rendered after server pick)
        window.onload = function(){{ document.getElementById('spinbtn').click(); }};
        </script>
        </body>
        </html>
        """
        components.html(html, height=520)
        # show server-side result too
        st.success(f"Result: {st.session_state['spin_result']}")
        if gained>0:
            st.info(f"+{gained} points added to your score.")
        else:
            st.info(st.session_state['spin_result'])
        return

    # show inactive wheel preview
    preview_labels = [o["label"] for o in options]
    preview_html = "<div style='text-align:center'>"
    preview_html += "<div style='width:300px;height:300px;margin:0 auto;border-radius:50%;border:8px solid #333;'></div>"
    preview_html += "<p>Press Spin Now to play!</p></div>"
    st.markdown(preview_html, unsafe_allow_html=True)

# ----------------------------
# Leaderboard page
# ----------------------------
def leaderboard_page():
    st.title("🏆 Leaderboard")
    df = pd.read_csv(LEADERBOARD_FILE)
    if df.empty:
        st.info("No scores yet — be the first!")
        return
    df = df.sort_values("points", ascending=False).reset_index(drop=True)
    df["RankTitle"] = df["points"].apply(get_title)
    st.dataframe(df)

# ----------------------------
# Reset / Retry
# ----------------------------
def reset_progress():
    username = st.session_state.get("username","")
    if username:
        # reset in progress file
        df = pd.read_csv(PROGRESS_FILE)
        if username in df['username'].values:
            df.loc[df['username']==username, ['points','streak','last_login','daily_done','tasks_done']] = [0,0,"",False,str([])]
            df.to_csv(PROGRESS_FILE,index=False)
        st.session_state.update({
            "points":0,"streak":0,"last_login":"","daily_done":False,"tasks_done":[],
            "maze_grid":None,"maze_items":None,"maze_pos":[0,0],"water_maze_items":None,"water_maze_pos":[0,0]
        })
        update_leaderboard(username)
        st.success("Progress reset for user.")
    else:
        st.error("No user loaded.")

# ----------------------------
# Login UI & main navigation
# ----------------------------
def login_page():
    st.title("🔐 EcoChallenge Login")
    usr = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if usr in USERS and USERS[usr] == pwd:
            st.session_state["login"] = True
            st.session_state["username"] = usr
            load_progress(usr)
            st.success(f"Welcome {usr} 🌿")
        else:
            st.error("Invalid credentials. Use student1/pass123 etc.")

def main_app():
    # sidebar: show user, save, reset
    st.sidebar.title("Player Controls")
    if not st.session_state["login"]:
        login_page()
        return
    st.sidebar.write(f"User: **{st.session_state['username']}**")
    st.sidebar.write(f"Points: **{st.session_state['points']}**")
    st.sidebar.write(f"Rank: **{get_title(st.session_state['points'])}**")
    st.sidebar.write(f"Streak: **{st.session_state['streak']}**")
    if st.sidebar.button("Save Progress"):
        save_progress(st.session_state['username'])
        update_leaderboard(st.session_state['username'])
        st.sidebar.success("Saved.")
    if st.sidebar.button("Reset / Retry"):
        reset_progress()

    page = st.sidebar.radio("Go to", [
        "Roadmap","Daily Challenge","Tasks","Maze","Water Maze",
        "Recycling Game","Quiz","Crossword","Spin the Wheel","Leaderboard"
    ])
    daily_fact()

    if page == "Roadmap":
        roadmap_page()
    elif page == "Daily Challenge":
        daily_challenge_page()
    elif page == "Tasks":
        tasks_page()
    elif page == "Maze":
        maze_page()
    elif page == "Water Maze":
        water_maze_page()
    elif page == "Recycling Game":
        recycling_game_page()
    elif page == "Quiz":
        quiz_page()
    elif page == "Crossword":
        crossword_page()
    elif page == "Spin the Wheel":
        spin_wheel_page()
    elif page == "Leaderboard":
        leaderboard_page()
    else:
        roadmap_page()

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    st.title("EcoChallenge Ultimate 🌱 — Play & Learn")
    main_app()
