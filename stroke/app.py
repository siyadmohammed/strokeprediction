try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    import os
    
    # Directly assign the API key here
    GROQ_API_KEY = "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"  # Replace with your actual API key
    
    # Check if API key is valid (not empty)
    if GROQ_API_KEY and GROQ_API_KEY != "":
        os.environ["GROQ_API_KEY"] = GROQ_API_KEY
        # Initialize LLM model
        model = ChatGroq(model="llama3-8b-8192")
        
        # Define the prompt template for stroke precautions
        system_template = """Based on a potential stroke detection:
        1. List FIVE immediate actions the person should take.
        2. Provide SEVEN important safety precautions to follow.
        3. Suggest FOUR lifestyle changes to reduce stroke risk.
        4. List THREE warning signs that require immediate medical attention.
        Format the information clearly and concisely, with a compassionate tone. The person is likely worried, so be reassuring while emphasizing the importance of medical care."""

        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "stroke precautions")]
        )

        # Chain the prompt and model
        precautions_chain = prompt_template | model
        GROQ_AVAILABLE = True
    else:
        GROQ_AVAILABLE = False
except (ImportError, Exception):
    GROQ_AVAILABLE = False
def get_stroke_precautions():
    """
    Invokes the LangChain-based ChatGroq model to get stroke precautions.
    
    Returns:
        dict: A structured dictionary containing the precautions.
    """
    try:
        response = precautions_chain.invoke({"user_input": "stroke precautions"})
        response_text = response.content.strip()
        
        # Parse the response into a structured dictionary
        precautions = {
            "immediate_actions": [],
            "safety_precautions": [],
            "lifestyle_changes": [],
            "warning_signs": []
        }
        
        # Parse the response
        lines = response_text.split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "immediate actions" in line.lower():
                current_section = "immediate_actions"
                continue
            elif "safety precautions" in line.lower():
                current_section = "safety_precautions"
                continue
            elif "lifestyle changes" in line.lower():
                current_section = "lifestyle_changes"
                continue
            elif "warning signs" in line.lower():
                current_section = "warning_signs"
                continue
                
            if current_section and line:
                # Remove numbering if present (e.g., "1. ", "• ")
                cleaned_line = line
                for prefix in ["• ", "- ", "* "]:
                    if line.startswith(prefix):
                        cleaned_line = line[len(prefix):]
                        break
                if line[0].isdigit() and line[1:3] in [". ", ") "]:
                    cleaned_line = line[3:]
                    
                precautions[current_section].append(cleaned_line)
        
        return precautions
        
    except Exception as e:
        print(f"Error getting stroke precautions: {str(e)}")