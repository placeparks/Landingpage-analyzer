from openai_functions import analyze_image_basic, generate_with_response_model
from prompt_template import anlysis_prompt
from ai_personas import persona_prompts_small
from models import SuggestionsModel
import web_screenshot
from performance_analysis import analyze_performance_directly
from mobile_responsiveness import check_mobile_responsiveness

url = "https://kainatportfolio.vercel.app/"

# Capture and upload the screenshot
captured_image_path = web_screenshot.capture_web_page_image(url, "screenshot_test.png")
image_url = web_screenshot.upload_to_imgur(captured_image_path)

# Perform direct performance analysis
performance_data = analyze_performance_directly(url)
print("Performance Analysis Completed")
    # Check mobile responsiveness
check_mobile_responsiveness(url)
print("Mobile Responsiveness Check Completed")

# Initialize an empty list to store all the results
all_persona_results = []

#loop through the list or personas and ask for evaluation
for persona in persona_prompts_small:
    for title, prompt in persona.items():
        print(f"Analyzing With: {title}...")
        persona_prompt = f"{prompt} {anlysis_prompt}"
        result = analyze_image_basic(image_url,persona_prompt)
        all_persona_results.append(result)
        print("Done------")

# Get the overall results
results_string = '\n'.join(all_persona_results)
final_prompt = f"Act as a Landing Page Expert Analyzer, please checkout the following feedback from different people about a landing page, extract 7-10 unique suggestions, and return them in a list in JSON format. Feedback: {results_string}"
overall_analysis = generate_with_response_model(final_prompt, SuggestionsModel)
print(overall_analysis.result)


