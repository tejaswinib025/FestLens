import streamlit as st
from db import init_db, insert_item, query_items, check_user, add_user
from utils import safe_filename, try_transcribe_audio, try_image_caption
import os, sqlite3, pandas as pd

# -------------------- INIT DB --------------------
os.makedirs("uploads/audio", exist_ok=True)
os.makedirs("uploads/image", exist_ok=True)
os.makedirs("uploads/video", exist_ok=True)
os.makedirs("uploads/text", exist_ok=True)
os.makedirs("exports", exist_ok=True)
init_db()   # ✅ ensure db is created before login

# -------------------- LOGIN --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "phone" not in st.session_state:
    st.session_state.phone = None

if not st.session_state.logged_in:
    st.title("Festival Log 🪔 - Login / Sign Up")
    choice = st.radio("Select option", ["Login", "Sign Up"])

    if choice == "Login":
        phone = st.text_input("Phone")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_user(phone, password):
                st.session_state.logged_in = True
                st.session_state.phone = phone
                st.success(f"Welcome {phone} ✅")
                st.rerun()   # rerun to load app
            else:
                st.error("Invalid phone or password")

    elif choice == "Sign Up":
        new_user = st.text_input("Choose a phone")
        new_pass = st.text_input("Choose a password", type="password")
        if st.button("Create Account"):
            if add_user(new_user, new_pass):
                st.success("✅ Account created! Please log in now.")
            else:
                st.error("⚠ Phone already exists. Try another.")
    st.stop()

# -------------------- APP --------------------
st.title("Festival Log 🪔")

# sidebar menu
page = st.sidebar.selectbox("📂 Menu", ["Upload new item", "Browse", "Export", "Leaderboard"])

# -------------------- UPLOAD --------------------
if page == "Upload new item":
    st.subheader("Upload new item")
    title = st.text_input("Title")
    festival = st.text_input("Festival")
    region = st.text_input("Region")
    language = st.text_input("Language", value="Telugu")
    tags = st.text_input("Tags (comma separated)")
    contributor = st.text_input("Contributor", value=st.session_state.phone or "")
    media_type = st.selectbox("Media type", ["audio", "video", "image", "text"])

    uploaded = None
    text = ""
    if media_type == "text":
        text = st.text_area("Text content")
    else:
        uploaded = st.file_uploader("Upload file", type=None)

    run_ai = st.checkbox("Run AI processing", value=False)

    if st.button("Save"):
        if media_type == "text":
            fname = safe_filename(title) + ".txt"
            path = os.path.join("uploads/text", fname)
            with open(path, "w", encoding="utf-8") as f: f.write(text)
        else:
            if uploaded is None:
                st.error("Please upload a file")
                st.stop()
            fname = safe_filename(uploaded.name)
            path = os.path.join(f"uploads/{media_type}", fname)
            with open(path, "wb") as f: f.write(uploaded.getbuffer())

        transcript, ai_caption, translation = None, None, None
        if run_ai:
            if media_type == "audio":
                transcript = try_transcribe_audio(path)
            elif media_type == "image":
                ai_caption = try_image_caption(path)

        item = {"title": title, "festival": festival, "region": region, "language": language,
                "media_type": media_type, "file_path": path, "transcript": transcript,
                "ai_caption": ai_caption, "translation": translation, "tags": tags,
                "contributor": contributor, "extra_json": "{}"}
        nid = insert_item(item)
        st.success(f"Saved! Entry ID: {nid}")

# -------------------- BROWSE --------------------
elif page == "Browse":
    st.subheader("Browse items")
    festival = st.text_input("Filter by Festival")
    language = st.text_input("Filter by Language")
    media_type = st.selectbox("Media type", ["All", "audio", "video", "image", "text"])
    search = st.text_input("Search text")

    results = query_items(
        {"festival": festival, "language": language, "media_type": media_type},
        search=search
    )

    st.write(f"Found {len(results)} items")
    for row in results:
        st.markdown(f"### {row['title']} ({row['festival']}) — {row['media_type']}")
        if row["media_type"] == "text":
            st.write(open(row["file_path"], "r", encoding="utf-8").read())
        elif row["media_type"] == "image":
            st.image(row["file_path"])
        elif row["media_type"] == "audio":
            st.audio(row["file_path"])
        elif row["media_type"] == "video":
            st.video(row["file_path"])
        if row["transcript"]:
            st.caption(f"Transcript: {row['transcript']}")
        if row["ai_caption"]:
            st.caption(f"Caption: {row['ai_caption']}")

# -------------------- EXPORT --------------------
elif page == "Export":
    st.subheader("Export dataset")
    if st.button("Export CSV/JSON"):
        conn = sqlite3.connect("festival_log.db")
        df = pd.read_sql_query("SELECT * FROM media", conn)
        conn.close()
        df.to_csv("exports/festival_log.csv", index=False)
        df.to_json("exports/festival_log.json", orient="records", force_ascii=False)
        st.success("Exported to exports/ folder")
        st.download_button("Download CSV", open("exports/festival_log.csv","rb"), "festival_log.csv")
        st.download_button("Download JSON", open("exports/festival_log.json","rb"), "festival_log.json")

# -------------------- LEADERBOARD --------------------
elif page == "Leaderboard":
    st.subheader("Leaderboard")
    conn = sqlite3.connect("festival_log.db")
    df = pd.read_sql_query("""
        SELECT COALESCE(contributor, 'Anonymous') as contributor,
               COUNT(*) as uploads
        FROM media
        GROUP BY contributor
        ORDER BY uploads DESC
    """, conn)
    conn.close()
    if df.empty:
        st.info("No contributions yet.")
    else:
        st.dataframe(df)
        st.bar_chart(df.set_index("contributor"))
