from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


def robot_tutor():
    lesson_name = input(str("lesson name?: "))
    technology_tech_course_name= input(str("technology_tech_course_name?: "))
    base_master_prompt = """
                You are an AI interviewer who when given a lesson name and technology/tech course name
                asks relevant questions on the given lesson name: 
                you ask questions in such format:
                
                you ask them relevant questions that the user can answer by writing text to you. (at max 3 such questions)
                You also ask them questions that user have to answer by writing code (at least 2 such questions)
                
                lesson name = {}
                technology/tech course name = {}
                
                you have to ask them questions one by one, and wait for users to answer the questions.
                
                before asking next question to the user, tell them whether their answer to the previous question was right or wrong.
                
                
                You must make sure that you dont ask the same question twice.
                begin!
                """.format(lesson_name,technology_tech_course_name)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                base_master_prompt,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    history = InMemoryChatMessageHistory()

    chain = prompt | ChatOpenAI() | StrOutputParser()

    wrapped_chain = RunnableWithMessageHistory(chain, lambda x: history)



    while True:
        human_input = input(str("human input: "))
        res = wrapped_chain.invoke(
            input={"input": human_input,"technology_tech_course_name":technology_tech_course_name,"lesson_name":lesson_name},
            config={"configurable": {"session_id": "new_tutor_2"}},
        )

        print(res)


if __name__ == "__main__":
    load_dotenv()
    robot_tutor()
