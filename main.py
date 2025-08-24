import google.generativeai as genai

# Store the Data Summary
detailed_analysis_summary = """**Comprehensive Analysis of MTA Subway Delays (2020-2024)**
1. Line-Level Analysis:

Top 5 Most Delayed Lines:

N: 171,808 delays

A: 164,413 delays

F: 154,176 delays

6: 150,206 delays

2: 137,412 delays

2. System-Wide Causal Analysis:

Top 5 General Delay Causes:

'Infrastructure & Equipment': 559,581 delays

'Police & Medical': 410,981 delays

'Planned ROW Work': 408,553 delays

'Crew Availability': 344,349 delays

'Operating Conditions': 316,193 delays

3. Infrastructure Deep Dive:

Top 5 Specific Infrastructure/Equipment Issues:

'Other - Sig' (likely Signals): 204,974 delays

'Rail and Roadbed': 77,210 delays

'Other - CE': 44,568 delays

'Service Delivery': 42,178 delays

'Other Infrastructure': 37,829 delays

4. Temporal Trend Analysis:

Peak Delays: The month with the highest number of delays was July 2022 with 46,482 delays.

Lowest Delays: The month with the fewest delays was May 2020 with 9,259 delays.

5. Case Study - The 'N' Line:

Top 3 Causes for the Most Delayed Line (N):

'Infrastructure & Equipment': 47,372 delays

'Planned ROW Work': 39,019 delays

'Crew Availability': 28,700 delays"""

# Configure API Key
# Replace "YOUR_API_KEY" with your actual Google Generative AI API key
genai.configure(api_key="AIzaSyBvO-x8pPR4mI1WoAKCXgjxxpit4UWgwPY")

# Create AI Prompt
prompt = """You are an expert NYC transit analyst with deep knowledge of subway operations, infrastructure, and urban planning. 

Based on the comprehensive MTA delay data provided, please perform the following analysis:

1. Executive Summary
- Provide a high-level overview of the key findings
- Identify the most critical issues affecting the subway system
- Highlight any surprising patterns or trends

2. Deeper Analysis of Root Causes
- Analyze why 'Infrastructure & Equipment' is the leading cause of delays
- Examine the relationship between different delay categories
- Investigate why the N line experiences the most delays
- Consider the impact of external factors (COVID-19, weather, etc.)

3. Actionable Recommendations
- Provide specific, implementable solutions for the top delay causes
- Suggest infrastructure improvement priorities
- Recommend operational changes that could reduce delays
- Consider short-term vs. long-term solutions

Please provide a comprehensive, professional analysis that would be suitable for transit officials and urban planners."""

# Instantiate Model and Generate
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, detailed_analysis_summary])
    
    # Print the Output
    print("=" * 80)
    print("AI-GENERATED MTA DELAY ANALYSIS")
    print("=" * 80)
    print(response.text)
    print("=" * 80)
    
except Exception as e:
    print(f"Error generating content: {e}")
    print("Please ensure you have:")
    print("1. A valid Google Generative AI API key")
    print("2. The google-generativeai library installed (pip install google-generativeai)")
    print("3. Proper internet connectivity") 