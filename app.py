# app.py (Streamlit UI - Cleaned Formatting with Fixed Step 4 Display)
import streamlit as st
import os
from graph import build_workflow, AgentState
from typing import TypedDict

# Global state setup
if 'app' not in st.session_state:
    try:
        # NOTE: The build_workflow function will now successfully load all agents
        st.session_state.app = build_workflow()
        st.success("🤖 BrandSync Studio Agents Initialized!")
    except Exception as e:
        st.error(f"Error initializing LangGraph: {e}")
        st.session_state.app = None

st.set_page_config(page_title="BrandSync Studio", layout="wide")
st.title("🖌️ BrandSync Studio: Autonomous AI Creative Agency")
st.markdown("Enter your creative brief and watch the **5-Agent Team** generate, review, and finalize your brand-consistent content.")

# --- UI Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    user_brief = st.text_area("Creative Brief:", "Create an engaging social media post for our new autonomous AI agency launch, focusing on speed and consistency.")
    
    if st.button("🚀 Launch Agent Workflow", use_container_width=True, type="primary"):
        if st.session_state.app is None:
            st.error("Workflow initialization failed. Cannot run.")
        elif user_brief:
            st.session_state.brief = user_brief
            st.session_state.running = True
            st.session_state.final_state = {}
            st.info("Workflow Started. See status timeline on the right.")
        else:
            st.warning("Please enter a creative brief.")

with col2:
    st.subheader("Workflow Status Timeline")
    
    if st.session_state.get('running', False) and st.session_state.app:
        progress_bar = st.progress(0)
        
        # Initial State
        initial_state = {"brief": st.session_state.brief, "revision_count": 0}
        
        step_count = 0
        max_steps = 7 

        status_container = st.container()
        
        with status_container:
            for i, step_state in enumerate(st.session_state.app.stream(initial_state)):
                step_count += 1
                progress_bar.progress(min(step_count / max_steps, 1.0))
                
                # Extracting the node name and state data
                node_name = list(step_state.keys())[0]
                state_data = step_state[node_name]
                
                st.markdown(f"**Step {step_count}: {node_name.upper()}**")
                
                if node_name == "strategist":
                    # FIX: Display strategy as clean markdown/text instead of st.json
                    st.markdown(f"**Strategy:** `{state_data.get('strategy')}`")
                elif node_name == "copywriter":
                    st.code(state_data.get('copy'), language='markdown')
                elif node_name == "designer":
                    st.markdown(f"Image Prompt: `{state_data.get('image_prompt')[:70]}...`")
                elif node_name == "brand_guardian":
                    # ✅ UPDATED: Clean display without error-like appearance
                    feedback = state_data.get('brand_feedback', '')
                    if 'REJECT' in feedback:
                        st.warning(f"🔄 **Revision Needed:** {feedback.replace('REJECT: ', '')}")
                    else:
                        st.success(f"✅ **Approved:** {feedback.replace('PASS: ', '')}")
                elif node_name == "compliance":
                    st.info(f"📋 **Report:** {state_data.get('compliance_report')}")

                st.session_state.final_state.update(state_data)
                
            st.session_state.running = False
            progress_bar.progress(1.0)
            st.success("✅ Workflow finished!")

# --- Display Final Output ---
if st.session_state.get('final_state') and 'final_output' in st.session_state.final_state:
    final_data = st.session_state.final_state['final_output']
    
    st.subheader("✅ Final Approved Content")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**Copy/Caption:**")
        st.code(final_data['copy'], language='markdown')
        st.markdown(f"**Total Revisions:** {st.session_state.final_state.get('revision_count', 0)}")
        
    with col4:
        # Display the correctly mocked placeholder image (no more PIL errors)
        image_path = final_data['image_path']
        if os.path.exists(image_path):
            st.image(image_path, caption="Generated Visual", use_container_width=True)
        else:
             st.warning(f"Image mock not found at: {image_path}")
        
    st.markdown("**Compliance Report:**")
    st.code(final_data['report'])