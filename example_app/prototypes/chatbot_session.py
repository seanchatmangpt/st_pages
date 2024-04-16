from abc import ABC, abstractmethod

import dspy
from datetime import datetime
from typing import List
from transitions import Machine

from dspygen.utils.cli_tools import chatbot, ChatbotAssistance
from dspygen.utils.dspy_tools import init_dspy
from soc.models.value_objects.message import Message
from soc.models.domain_models.conversation import Conversation
from soc.models.domain_models.user import User

class ChatbotResponseGenerator(ABC):
    @abstractmethod
    def generate_response(self, user_message: str, conversation: Conversation) -> str:
        pass

class ChatbotSession:
    def __init__(self, conversation_id: str, user: User, chatbot: User, response_generator: ChatbotResponseGenerator):
        self.conversation_id = conversation_id
        self.user = user
        self.chatbot = chatbot
        self.conversation = Conversation(conversation_id=conversation_id, messages=[])
        self.state_machine = Machine(
            model=self,
            states=['idle', 'conversing', 'completed'],
            initial='idle',
            transitions=[
                {'trigger': 'start_conversation', 'source': 'idle', 'dest': 'conversing'},
                {'trigger': 'end_conversation', 'source': 'conversing', 'dest': 'completed'}
            ]
        )
        self.response_generator = response_generator

    def add_message(self, text: str, sender: User):
        message = Message(message_id=str(datetime.now()), text=text, user=sender)
        self.conversation.messages.append(message)

    def get_last_messages(self, count: int) -> List[Message]:
        return self.conversation.messages[-count:]

    def process_user_message(self, text: str):
        self.add_message(text, self.user)
        response = self.response_generator.generate_response(text, self.conversation)
        self.add_message(response, self.chatbot)

    def start_conversation(self):
        self.state = 'conversing'
        self.add_message("Welcome to the Chatbot Assistant!", self.chatbot)

    def end_conversation(self):
        self.state = 'completed'
        self.add_message("Thank you for using the Chatbot Assistant!", self.chatbot)


class ChatbotSessionRepository(ABC):
    @abstractmethod
    def load_session(self, conversation_id: str, user: User, chatbot: User, response_generator: ChatbotResponseGenerator) -> ChatbotSession:
        pass

    @abstractmethod
    def save_session(self, session: ChatbotSession):
        pass

class YAMLChatbotSessionRepository(ChatbotSessionRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_session(self, conversation_id: str, user: User, chatbot: User, response_generator: ChatbotResponseGenerator) -> ChatbotSession:
        try:
            with Conversation.io_context(file_path=self.file_path) as conversation:
                session = ChatbotSession(conversation_id, user, chatbot, response_generator)
                session.conversation = conversation
                return session
        except FileNotFoundError:
            session = ChatbotSession(conversation_id, user, chatbot, response_generator)
            return session

    def save_session(self, session: ChatbotSession):
        with Conversation.io_context(file_path=self.file_path) as conversation:
            conversation.id = session.conversation_id
            conversation.messages = session.conversation.messages

class ChatbotService:
    def __init__(self, session_repository: ChatbotSessionRepository, response_generator: ChatbotResponseGenerator):
        self.session_repository = session_repository
        self.response_generator = response_generator

    def start_conversation(self, conversation_id: str, user: User, chatbot: User):
        session = self.session_repository.load_session(conversation_id, user, chatbot, self.response_generator)
        session.start_conversation()
        session.add_message("Welcome to the Chatbot Assistant!", chatbot)
        self.session_repository.save_session(session)

    def process_user_message(self, conversation_id: str, user: User, chatbot: User, text: str):
        session = self.session_repository.load_session(conversation_id, user, chatbot, self.response_generator)
        session.process_user_message(text)
        self.session_repository.save_session(session)

    def end_conversation(self, conversation_id: str, user: User, chatbot: User):
        session = self.session_repository.load_session(conversation_id, user, chatbot, self.response_generator)
        session.end_conversation()
        session.add_message("Thank you for using the Chatbot Assistant!", chatbot)
        self.session_repository.save_session(session)

    def get_last_messages(self, conversation_id: str, user: User, chatbot: User, count: int) -> List[Message]:
        session = self.session_repository.load_session(conversation_id, user, chatbot, self.response_generator)
        return session.get_last_messages(count)

# Example usage
class SimpleChatbotResponseGenerator(ChatbotResponseGenerator):
    def generate_response(self, user_message: str, conversation: Conversation) -> str:
        return f"You said: {user_message}"


class RealChatbotResponseGenerator(ChatbotResponseGenerator):
    def generate_response(self, user_message: str, conversation: Conversation) -> str:
        init_dspy()
        qa = dspy.ChainOfThought(ChatbotAssistance)
        response = qa(question=user_message, context="Socratic Tutor AI", conversation_history=conversation.history()).answer
        return response
