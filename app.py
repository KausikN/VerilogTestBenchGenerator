"""
Stream lit GUI for hosting VerilogTestBenchGenerator
"""

# Imports
import os
import json
import streamlit as st

from VerilogTestBenchGenerator import *

# Main Vars
config = json.load(open("./StreamLitGUI/UIConfig.json", "r"))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    "Choose one of the following",
        tuple(
            [config["PROJECT_NAME"]] + 
            config["PROJECT_MODES"]
        )
    )
    
    if selected_box == config["PROJECT_NAME"]:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(" ", "_").lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config["PROJECT_NAME"])
    st.markdown("Github Repo: " + "[" + config["PROJECT_LINK"] + "](" + config["PROJECT_LINK"] + ")")
    st.markdown(config["PROJECT_DESC"])

    # st.write(open(config["PROJECT_README"], "r").read())

#############################################################################################################################
# Repo Based Vars
PATHS = {
    "cache": "StreamLitGUI/CacheData/Cache.json",
}

# Util Vars
CACHE = {}

# Util Functions
def LoadCache():
    global CACHE
    CACHE = json.load(open(PATHS["cache"], "r"))

def SaveCache():
    global CACHE
    json.dump(CACHE, open(PATHS["cache"], "w"), indent=4)

# Main Functions


# UI Functions


# Repo Based Functions
def testbench_generator():
    # Title
    st.header("Verilog Test Bench Generator")

    # Prereq Loaders

    # Load Inputs
    USERINPUT_VerilogFile = st.file_uploader("Upload Verilog File", type=["v"])
    USERINPUT_ModuleName = st.text_input("Module Name", value="")
    cols = st.columns(2)
    USERINPUT_TimeDelay = cols[0].number_input("Time Delay", value=0)
    USERINPUT_ClockDelay = cols[1].number_input("Clock Delay", value=0)
    cols = st.columns(2)
    USERINPUT_AllTestCases = cols[0].checkbox("All Test Cases", value=False)
    USERINPUT_NoOfTestCases = 1
    if not USERINPUT_AllTestCases: USERINPUT_NoOfTestCases = cols[1].number_input("Number of Test Cases", min_value=1, value=1)

    # Process Check
    USERINPUT_Process = st.checkbox("Stream Process", value=False)
    if not USERINPUT_Process: USERINPUT_Process = st.button("Process")
    if not USERINPUT_Process: st.stop()
    # Process Inputs
    modulename = USERINPUT_ModuleName
    timedelay = USERINPUT_TimeDelay
    clockdelay = USERINPUT_ClockDelay
    nooftestcases = USERINPUT_NoOfTestCases
    alltestcases = USERINPUT_AllTestCases
    VERILOG_CONTENTS = str(USERINPUT_VerilogFile.read())
    ResetAllVars()
    TEST_BENCH_CONTENTS = InputOutputVerilogParser(
        VERILOG_CONTENTS,
        modulename,
        timedelay, clockdelay,
        nooftestcases, alltestcases
    )

    # Display Outputs
    st.subheader("Test Bench")
    st.download_button(
        label="Download Test Bench",
        data=TEST_BENCH_CONTENTS,
        file_name=f"{modulename}_tb.v",
        mime="text/plain"
    )
    st.code(TEST_BENCH_CONTENTS, language="verilog")
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()