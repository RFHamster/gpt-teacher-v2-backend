from app.agents.teacher_agent import call_teacher_agent
from app.agents.teacher_agent.model import AgentInput
    

def main():
	print('Hello from gpt-teacher-backend!')

def test_agent_reponse():
    agent_input = AgentInput(
        problem_title="Soma de Dois Números",
        problem_description="Dado dois números, retorne a soma deles.",
        student_code="def soma(a, b):\n    return a - b",
        user_message="Meu código não está funcionando. O que há de errado?",
		session_id="12345"  
    )

    response = call_teacher_agent(agent_input)
    print("Resposta do Agente Professor:")
    print(response)
	
def test_agent_memory():
    agent_input = AgentInput(
        problem_title="Soma de Dois Números",
        problem_description="Dado dois números, retorne a soma deles.",
        student_code="def soma(a: int, b: int) -> int:\n    return a + b",
        user_message="era assim que eu tinha que fazer? O que você lembra do meu código anterior?",
		session_id="12345"  
    )

    response = call_teacher_agent(agent_input)
    print("Resposta do Agente Professor:")
    print(response)
    

if __name__ == '__main__':
	main()
	test_agent_reponse()
	test_agent_memory()
