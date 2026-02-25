#FeedBack analyser


#import
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import re
import time
#Step -1: Page_setup with CSS
st.set_page_config(
    page_title="MyFeeds@ZOMATO.com",
    page_icon=":postbox:",
    layout="wide",
    initial_sidebar_state="expanded",
       menu_items={
     'Get Help': 'https://www.extremelycoolapp.com/help',
     'Report a bug': "https://www.extremelycoolapp.com/bug",
     'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title(":red[Zomato|]Feeds:pizza:")
st.markdown('''
            <style>  
                .stApp{
                    background-color: white;
                    color: green;
                    font-style: italic;
                    font-family: Calibri;
                }
                h3{
                    color: red;
                }
                h4{
                    color: violet;
                }
                h6{
                    color: black;
                }
                #price{
                    font-size:30px;
                    font-weight:bolder;
                }
                .features{
                    display:flex;
                }
                img{
                    border-radius:24px;    
                }
                .Product{
                    background-color: white;
                }
                .Product_items{
                }
                h4{
                    color: violet;
                }
                h6{
                    color: black;
                }
                #price{
                    font-size:30px;
                    font-weight:bolder;
                }
                .features{
                    display:flex;
                }
                }


            </style>
            ''', unsafe_allow_html=True)
#Step -2: Data Intialization and LLM
if 'db' not in st.session_state:
    st.session_state.db = []
if 'p' not in st.session_state:
    st.session_state.p = {
        "Pizza"     : {
            "ts" : 5.0,
            "c"  : 1,
            "icon" : "https://www.schwartz.co.uk/-/media/project/oneweb/schwartz/recipes/recipe_image_update/march_18_2025/easy_pizza_recipe_800x800.webp?rev=217b39d7488a4aa7947174d6e475219f&vd=20250325T174436Z&extension=webp&hash=36F310B7BA2EA4491AADEC213844DF8B",
            "data" : "Cheese, Mushroom, Chiken",
            "vnv" : "veg and non-veg",
            "type": "breads",
            "price": 549.54
        },
        "Burger"    : {
            "ts" : 4,
            "c"  : 1,
            "icon" : "https://images.themodernproper.com/production/posts/2016/ClassicCheeseBurger_9.jpg?w=1200&h=1200&q=60&fm=jpg&fit=crop&dm=1749310239&s=463b18fc3bb51dc5d96e866c848527c4",
            "data" : "Cheese, Mushroom, Chiken",
            "vnv" : "veg and non-veg",
            "type": "breads",
            "price": 349.54
        },
        "French fries" : {
            "ts" : 2.0,
            "c"  : 1,
            "icon" : "https://kirbiecravings.com/wp-content/uploads/2019/09/easy-french-fries-1.jpg",
            "data" : "rosted",
            "vnv" : "veg",
            "type": "snacks",
            "price": 249.54
        },
        "Nuggets"   : {
            "ts" : 5.0,
            "c"  : 1,
            "icon" : "https://www.acozykitchen.com/wp-content/uploads/2025/12/HomemadeChickenNuggets-06.jpg",
            "data" : "Mushroom, Chiken",
            "vnv" : "veg and non-veg",
            "type": "snacks",
            "price": 149.54
        },
        "Biryanis"  : {
            "ts" : 3.8,
            "c"  : 1,
            "icon" : "https://www.cookwithmanali.com/wp-content/uploads/2019/09/Vegetable-Biryani-Restaurant-Style.jpg",
            "data" : "Veg, Mushroom, Chiken",
            "vnv" : "veg and non-veg",
            "type": "main Menu",
            "price": 449.54
        }
    }

#sentiment analysis function
def analyse(t):
    t = t.lower()
    p = sum(t.count(w) for w in ["delicious", "tasty", "yummy", "good", "amazing", "awesome"])
    n = sum(t.count(w) for w in ["bad", "worst", "awful", "disgusting", "horrible", "unpleasant"])
    if p > n:
        return "Positive", "#008000"
    elif n > p:
        return "Negative", "#FF0000"
    else:
        return "Neutral", "#808080"


#Step -3: UI Page with CSS
option = st.sidebar.radio(":red[Menu]", ["Feedback", "Analytics"])


if option == "Feedback":
    st.badge("My Dishes & feedback", color="violet")
    cols = st.columns(5)
    for i, (name, info) in enumerate(st.session_state.p.items()):
        with cols[i]:
            avg = round(info['ts'] / info['c'])
            st.markdown(f'''
                    <section class="Product_items">
                        <div name="Product">
                        <img src="{info['icon']}">
                        <h3> {name} </h3> <p> {"🌟"*int(avg)}</p>
                        <div class="features" style="display:flex;>
                              <span> {info['vnv']}</span>
                              <span> {info['type']} </span>
                        </div>
                         <h6> {info['data']}</h6>
                        <h1 id="price" > ₹{f"{info['price']}"} </h1>
                        </div>
                    </section>
                    
               ''', unsafe_allow_html=True)
            st.badge(f"{info['price']}")
            st.expander("Reviews")
            


    st.divider()
    st.badge("Feedback Form", color="red")
    c1, c2 = st.columns(2)
    with c1:
        em = st.text_input("email:")
        pr = st.selectbox("Select Item to review", ["--select--", "Pizza", "Burger", "French fries", "Nuggets", "Biryanis"])
        sr = st.select_slider("Rate the Item", [1,2,3,4,5],3)
    with c2:
        tx = st.text_area("write your Feedback,", height=180)
        if st.button("Submit"):
            if not re.match(r"^|a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", em):
                st.error("Use proper email format name@domain.com")
            elif any(r for r in st.session_state.db if r['prod'] == em and r['item'] == pr):
                st.warning(f"Email {em} has already reviewed {pr}")
            elif tx:
                sent,col = analyse(tx)
                st.session_state.db.append({
                    "email": em,
                    "prod": pr,
                    "stars": sr,
                    "txt": tx,
                    "sent": sent,
                    "col": col
                })
                st.session_state.p[pr]['c'] += 1
                st.success("Feedback submitted successfully!")
                time.sleep(1)
                st.rerun()
                
elif option == "Analytics":
    st.badge("Reviews & Analytics", color="blue")
#Step -4: Analytics


