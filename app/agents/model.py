from langchain_groq import ChatGroq

def get_model(student_code_complexity):
    match student_code_complexity:
        case "INICIANTE":   
            return get_low_groq()
        case "INTERMEDIARIO":
            return get_mid_groq()
        case "AVANCADO":
            return get_high_groq()


def get_low_groq():
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0.7, max_tokens=1000)
    
def get_mid_groq():
    return ChatGroq(model="mixtral-8x7b-32768", temperature=0.5, max_tokens=1500)   

def get_high_groq():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=2000) 


