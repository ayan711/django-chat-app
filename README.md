# Real-time Chat Application with Django Channels

A real-time chat application built using Django, Django Channels, and WebSockets. The application enables users to have private one-on-one conversations in real-time.

## Architecture

### System Architecture

![System Architecture](./websocket_project/docs/Architecture_Diagram.png)

### Message Flow

![Message Flow](./websocket_project/docs/Flow_Diagram.png)

## Features

- Real-time messaging using WebSockets
- Private one-on-one chat rooms
- Message persistence in database
- User authentication
- Clean and responsive UI using Tailwind CSS
- Message timestamps
- Online status indicators
- Visual message alignment (right for sent, left for received)

## Technical Stack

- **Backend**: Django 4.0+
- **WebSockets**: Django Channels 4.0+
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Database**: SQLite (default)
- **Protocol**: WebSocket for real-time communication

## Data Flow

1. **Authentication Flow**:

   - User accesses the application
   - Django authentication middleware checks login status
   - If not logged in, redirects to login page
   - After successful login, redirects to user list

2. **Chat Initialization Flow**:

   - User selects another user to chat with
   - Django creates/retrieves chat room
   - WebSocket connection established for real-time updates
   - Previous messages loaded from database

3. **Message Flow**:
   - User sends message via WebSocket
   - Consumer receives message
   - Message saved to database
   - Message broadcasted to room participants
   - Receivers' UI updated in real-time

## Setup and Installation

1. Clone the repository:

- git clone <repository-url>

2. Create and activate virtual environment:
   python -m venv env
   source env/bin/activate # On Windows: env\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run migrations:
   python manage.py migrate

5. Start the server:
   daphne -p 8000 websocket_project.asgi:application

6. Access the application:
   http://localhost:8000/chat/

## Usage

1. Access the application at `http://localhost:8000`
2. Log in with your credentials
3. Select a user from the list to start chatting
4. Type messages in the input field and press Enter or click Send
5. Messages appear in real-time for both participants

## Security Considerations

- WebSocket connections are authenticated
- Chat rooms are private between participants
- SQL injection protection via Django ORM
- XSS protection in templates
- CSRF protection for HTTP requests

## Future Enhancements

- Group chat functionality
- Message read receipts
- File sharing capabilities
- User typing indicators
- Message reactions
- Message search functionality
- Push notifications

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
