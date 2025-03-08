
from src.utils.logger import logging
from src.modules.history.model import Conversation
from src.modules import (GuardAgent, 
                         ClassificationAgent, 
                         StoryAgent, 
                         DeepTalkAgent, 
                         HappyAgent, 
                         SurpriseAgent, 
                         NormalAgent, 
                         AgentProtocol)


def main():
    manage_conversation = Conversation()
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    happy_agent = HappyAgent()
    surprise_agent = SurpriseAgent()
    normal_agent = NormalAgent()

    sad_agent: dict[str, AgentProtocol] = {
        "story": StoryAgent(),
        "deep_talk": DeepTalkAgent()
    }

    while True:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print('----------Print messages----------')

        prompt = input("User: ")
        
        conversation_id = manage_conversation.update_chat_conversation(
            bot_id='bot2',
            user_id='kiet2',
            message=prompt
        )

        conversation_messages = manage_conversation.get_conversation_messages(
            conversation_id=conversation_id
        )

        history = conversation_messages[-5:-1]

        guard_agent_response = guard_agent.get_response(
            history=history,
            messages=prompt
        )
        
        if guard_agent_response['memory']['guard_decision'] == 'not_allowed':
            continue

        classification_agent_response = classification_agent.get_response(
            history=history,
            messages=prompt
            )
        
        logging.info('----------------------------------- before')

        if classification_agent_response['content'] != '':
            response = classification_agent_response
        
        
        else:
            decisions = classification_agent_response["memory"]["classification_agent"]
            for decision in decisions:
                first_key = next(iter(decision))  
                
                logging.info(f'----------------------------------- {first_key}')

                if first_key == "not_vague" and decision[first_key] == "yes":
                    logging.info(f"Emotion: {decision['detailed']['emotion']}, Next Move: {decision['detailed']['next_move']}")
                    emotion = decision['detailed']['emotion']
                    next_move = decision['detailed']['next_move']

                    if emotion == 'sad':
                        agent = sad_agent[next_move]
                        response = agent.get_response(history=history,
                                                      messages=prompt)
                        
                    else:
                        pass
        
        manage_conversation.update_chat_conversation(
            bot_id='bot2',
            user_id='kiet2',
            message=response
        )


        logging.info(f'---------- Response: {response} ----------')
                    

        # agent = agent_dict[chosen_agent]

        # response = agent.get_response(history=history, messages=prompt)

if __name__ == "__main__":
    main()