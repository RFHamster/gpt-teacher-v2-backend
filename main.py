from app.agents.teacher_agent import call_teacher_agent
from app.agents.teacher_agent.model import AgentInput

def main():
    print("Hello World!")

def tests():
    agent_input = AgentInput(
        problem_title="Soma de dois números",
        problem_description="Crie uma função que some A e B",
        is_sandbox=False,
        student_code="def soma(a, b): return a + b",
        user_message="Olá, professor! Meu código está certo?",
        session_id="12345",
        student_id="student_001"
    )

    response = call_teacher_agent(agent_input)
    print("Response from teacher agent:")
    print(response)

    agent_input = AgentInput(
        problem_title="Soma de dois números",
        problem_description="Crie uma função que some A e B",
        is_sandbox=False,
        student_code="def soma(a, b): return a + b",
        user_message="Nao entendi, pode me explicar melhor?",
        session_id="12345",
        student_id="student_001"
    )

    response = call_teacher_agent(agent_input)
    print("Response from teacher agent:")
    print(response)

    agent_input = AgentInput(
        problem_title="Soma de dois números",
        problem_description="Crie uma função que some A e B",
        is_sandbox=False,
        student_code="def soma(a, b): return a + b",
        user_message="Nao entendi, pode me explicar melhor?",
        session_id="12345",
        student_id="student_001"
    )

    response = call_teacher_agent(agent_input)
    print("Response from teacher agent:")
    print(response)

    agent_input = AgentInput(
        problem_title="Soma de dois números",
        problem_description="Crie uma função que some A e B",
        is_sandbox=False,
        student_code="def soma(a, b): return a + b",
        user_message="como eu faço para testar minha função?",
        session_id="12345",
        student_id="student_001"
    )
            
    response = call_teacher_agent(agent_input)
    print("Response from teacher agent:")
    print(response)


if __name__ == "__main__":
    main()
    tests()
