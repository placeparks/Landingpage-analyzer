import openai
import streamlit as st
from openai_functions import analyze_image_basic, generate_with_response_model
from prompt_template import anlysis_prompt  # Ensure this is correctly named
from ai_personas import persona_prompts_small
from models import SuggestionsModel
import web_screenshot
from performance_analysis import analyze_performance_directly
from mobile_responsiveness import check_mobile_responsiveness
import os

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def calculate_overall_score(performance_data):
    # Example metrics contained in performance_data
    load_time = performance_data.get('loadTime', 0)
    time_to_interactive = performance_data.get('timeToInteractive', 0)
    speed_index = performance_data.get('speedIndex', 0)
    
    # Define maximum thresholds for good performance
    max_good_load_time = 3000  # 3 seconds
    max_good_tti = 5000  # 5 seconds
    max_good_speed_index = 3000  # 3 seconds
    
    # Calculate score contributions from each metric
    load_time_score = max(0, (max_good_load_time - load_time) / max_good_load_time)
    tti_score = max(0, (max_good_tti - time_to_interactive) / max_good_tti)
    speed_index_score = max(0, (max_good_speed_index - speed_index) / max_good_speed_index)
    
    # Calculate overall score (example: simple average of the three scores)
    overall_score = (load_time_score + tti_score + speed_index_score) / 3 * 100  # Scale to 100
    
    return overall_score


def main():
    st.sidebar.title("Landing Page Analyzer")
    st.sidebar.write("""
        Welcome! Follow the steps in the sidebar to analyze a landing page.
        You can provide an image URL directly, or enter a URL to capture a screenshot of the page.
    """)

    method = st.sidebar.radio(
        "Choose your method to provide the image:",
        ('Public URL', 'URL to Capture')
    )

    if method == 'Public URL':
        public_url = st.sidebar.text_input("Enter the public URL of the image:")
        if public_url:
            analyze_image(public_url)

    elif method == 'URL to Capture':
        capture_url = st.sidebar.text_input("Enter the URL to capture the webpage:")
        if capture_url:
            with st.spinner('Capturing webpage...'):
                try:
                    captured_image_path = web_screenshot.capture_web_page_image(capture_url, "screenshot_test.png")
                    image_url = web_screenshot.upload_to_imgur(captured_image_path)
                    if image_url:
                        st.success('Webpage captured successfully!')
                        analyze_image(image_url, capture_url)
                    else:
                        st.error('Failed to capture webpage. Please check the URL and try again.')
                except Exception as e:
                    st.error(f'Error capturing or uploading image: {e}')

def analyze_image(image_url, capture_url=None):
    st.image(image_url, caption='Image for Analysis', use_column_width=True)
    
    if capture_url:
        try:
            performance_data = analyze_performance_directly(capture_url)
            performance_score = calculate_overall_score(performance_data)
            st.write(f"Performance Score: {performance_score}")
        except Exception as e:
            st.error(f"Failed to perform performance analysis: {e}")
        
        try:
            mobile_responsive_result = check_mobile_responsiveness(capture_url) or "No mobile responsiveness issues detected."
            st.write("Mobile Responsiveness Check Completed")
            st.write(mobile_responsive_result)
        except Exception as e:
            st.error(f"Failed to check mobile responsiveness: {e}")

    all_persona_results = []
    for persona in persona_prompts_small:
        for title, prompt in persona.items():
            try:
                st.write(f"Analyzing with persona: {title}...")
                persona_prompt = f"{prompt} {anlysis_prompt}"
                result = analyze_image_basic(image_url, persona_prompt)
                all_persona_results.append(result)
            except Exception as e:
                st.error(f"Failed to analyze image with persona {title}: {e}")

    results_string = '\n'.join(all_persona_results)
    final_prompt = (
        "Act as a Landing Page Expert Analyzer, please checkout the following feedback "
        "from different people about a landing page, extract 7-10 unique suggestions, "
        "and return them in a list in JSON format. Feedback: "
        f"{results_string}"
    )
    try:
        overall_analysis = generate_with_response_model(final_prompt, SuggestionsModel)
        st.write("Overall Analysis:")
        for suggestion in overall_analysis.result:
            st.markdown(f"- {suggestion}")
    except Exception as e:
        st.error(f"Failed to generate overall analysis: {e}")

if __name__ == "__main__":
    main()

# Add custom CSS for footer
footer_style = """
position: fixed;
left: 0;
bottom: 0;
width: 100%;
text-align: center;
padding: 10px;
background-color: rgba(255, 255, 255, 0.5);  /* Semi-transparent light background */
color: #000;                                  /* Dark text for visibility */
border-top: 1px solid #000;                   /* Border to distinguish the footer */
z-index: 1000;                                /* Ensures it stays on top of other elements */
"""

# Footer
st.markdown(
    '<div style="{}">Developed by Mirac.eth<br>Contact: mirac.eth@ethereum.email</div>'.format(footer_style),
    unsafe_allow_html=True
)