import streamlit as st
from firebase.firebase_utils import write_task_item
import datetime
import glob

import random
import json

# sample an item
# item = prompt + 2 responses 
# ask them to rate each response
# submit the form
# write the response + item to the database

def sample_index():
    fn = './data/available_inds_12_12.json'
    with open(fn, 'r') as f:
        inds = json.load(f)
    if len(inds) <5:
        print("resetting inds")
        inds = list(range(0, 3784))
        
    random.shuffle(inds)

    # select an index
    sampled_ind = inds.pop(0)

    # save the new inds
    with open(fn, 'w') as f:
        json.dump(inds, f)
    
    return sampled_ind



def sample_item(ind):
    #fn = f'./data/processed_12_12/{ind}.json'
    fns = glob.glob(f'./data/processed_12_12/*.json')
    fn = fns[ind]
    with open(fn, 'r') as f:
        item = json.load(f)
    return item



with st.form("feedback-form"):

    # sample an item
    ind = sample_index()
    item = sample_item(ind)
    prompt = item["human_readable_transcript"]
    responses = item["responses"]

    response_keys = list(responses.keys())
    random.shuffle(response_keys)

    item_id = item["prompt_id"]

    feedback_object = {}

    def capture_score():
        feedback_object["responses"] = responses

        feedback_object["response_ratings"] = {}

        for response_key in response_keys:
            feedback_object["response_ratings"][response_key] = int(st.session_state[response_key])

        feedback_object["user_name"] = st.session_state["user_name"]
        feedback_object["human_readable_transcript"] = prompt
        feedback_object["rewrite"] = st.session_state["rewrite"]
        feedback_object["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        feedback_object["item_id"] = item_id

        # write to firebase
        write_task_item(feedback_object, "12-12-feedback")

        # reset all fields except name
        for response_key in response_keys:
            st.session_state[response_key] = "1"
        st.session_state["rewrite"] = None

    user_name = st.text_input("Enter your name", key="user_name")

    st.write("**Please read the following transcript of a conversation between a patient and a nurse. There may be errors in the transcript - do your best to understand the conversation, and then rate the responses that follow**")
    st.write(prompt)

    st.write("**Here are possible next responses from the nurse in the conversation. Rate each response on a scale of 1 to 7 for overall subjective quality.**")

    for response_key in response_keys:
        st.radio(responses[response_key], ("1", "2","3","4","5","6","7"), key=response_key, horizontal=True)

    form_feedback = st.text_input("Write your ideal response:", key="rewrite")

    submit_button = st.form_submit_button(label='Submit', on_click=capture_score)

