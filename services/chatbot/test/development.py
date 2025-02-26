import logging

from src.modules.history.model import Conversation
from src.modules import GuardAgent, ClassificationAgent


def main():
    manage_conversation = Conversation()
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()

    while True:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print('----------Print messages----------')

        prompt = input("User: ")
        
        conversation_id = manage_conversation.update_chat_conversation(
            bot_id='bot1',
            user_id='kiet',
            message=prompt
        )

        logging.info(f"Conversation_id: {conversation_id}")

        conversation_messages = manage_conversation.get_conversation_messages(
            conversation_id=conversation_id
        )
        logging.info(f'Conversation messages: {conversation_messages}')

        history = conversation_messages[-5:-1]

        guard_agent_response = guard_agent.get_response(
            history=history,
            message=prompt
        )

        print(f'Guard Agent Response: {guard_agent_response}')
        if guard_agent_response['memory']['guard_decision'] == 'not_allowed':
            continue

        classification_agent_response = classification_agent.get_response(
            history=history,
            message=prompt
            )
        
        print(f'Classification Response: {classification_agent_response}')
        # chosen_agent = classification_agent_response['memory']['classification_agent']

        # logging.info(f"Chosen Agent: {chosen_agent}")

        # agent = agent_dict[chosen_agent]
        # response = agent.get_response(messages)

        # logging.info(f"Response: {response}")

        # messages.append(guard_agent_response)

if __name__ == "__main__":
    main()