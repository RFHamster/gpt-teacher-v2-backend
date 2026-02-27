from langchain_groq import ChatGroq

def get_groq_model(TASK_DIFFICULTY):
    match TASK_DIFFICULTY:
        case "LOW":   
            return get_low_groq()
        case "MEDIUM":
            return get_mid_groq()
        case "HIGH":
            return get_high_groq()
        

def get_response_from_groq_model(prompt, config, brain):
    response = brain.invoke(
        prompt=prompt, 
        config=config
    ).content
    
    return response

def get_low_groq():
    return ChatGroq(model="llama-3.3-8b", temperature=0.7, max_tokens=1000)
    
def get_mid_groq():
    return ChatGroq(model="mixtral-8x7b-32768", temperature=0.5, max_tokens=1500)   

def get_high_groq():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=2000) 