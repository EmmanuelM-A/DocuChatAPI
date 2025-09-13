"""
Abstractions and plans for the Chatbot service.
"""


class AuthService:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def register_user(self):
        pass

    def login_user(self):
        pass

    def logout_user(self):
        pass

    def refresh_access_token(self):
        pass


class UserServices:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def get_user_details(self):
        pass

    def update_user_details(self):
        pass

    def get_user_token_usage(self):
        pass


class ChatbotSessionServices:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def get_user_chat_sessions(self):
        pass

    def create_chat_session(self):
        pass

    def get_chat_session_details(self):
        pass

    def delete_chat_session_and_associated_content(self):
        pass

    def update_chat_session_details(self):
        pass


class DocumentManagementServices:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def upload_file_to_chat_session(self):
        pass

    def get_files_uploaded_to_chat_session(self):
        pass

    def download_uploaded_file_from_chat_session(self):
        pass

    def delete_upload_file_from_chat_session(self):
        pass


class FileUploadService:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def upload_file(self):
        pass

    def upload_files(self):
        pass

    def get_user_files(self):
        pass

    def delete_file(self):
        pass

    def delete_files(self):
        pass


class ChatbotService:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def chat_with_chatbot_from_chat_session(self, question):
        pass

    def get_messages_from_chat_session(self):
        pass

    def view_chat_message_from_chat_session(self, msg_id):
        pass


class ChatbotUtilService:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def export_chat_session_history_as_pdf(self):
        pass

    def export_chat_session_history_as_txt(self):
        pass


class SearchServices:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def search_chat_sessions_by_keyword(self, keyword):
        pass

    def search_chat_sessions_messages_by_keyword(self, keyword):
        pass


class DashboardServices:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def get_user_dashboard_summary(self):
        pass

    def get_dashboard_tokens(self):
        pass

    def get_dashboard_limits(self):
        pass
