# Top AI Tools Agent Project

This project aims to build an agent that collects information about "top AI tools" from various search engines (Google, Bing, Baidu), stores this data in an SQLite database, and presents it through a React-based web interface. The backend uses FastAPI and Langchain to orchestrate the data collection and storage, while the frontend provides a user interface to interact with the agent and view the collected tools.

## Project Components

1.  **`agent-server` (Python/FastAPI/Langchain)**:
    *   Responsible for web scraping using Playwright and BeautifulSoup.
    *   Stores collected data in an SQLite database.
    *   Exposes a REST API for the frontend.
    *   Utilizes a Langchain agent to intelligently search for and categorize AI tools.
2.  **`web` (React)**:
    *   A web application to display the collected AI tools.
    *   Allows users to trigger the Langchain agent with specific search tasks.
    *   Provides a user-friendly interface for browsing and interacting with the data.

## Features

*   **Multi-Engine Scraping**: Gather data from Google, Bing, and Baidu search engines.
*   **Data Persistence**: Store collected data in a local SQLite database (`ai_tools.db`).
*   **Langchain Agent**: An intelligent agent that uses search tools and a database tool to find and store AI tool information.
*   **Interactive UI**: A React interface for exploring AI tools and running the agent.
*   **Search & Filter**: (Planned for future enhancement) Functionality to easily find specific tools within the collected data.

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Top-AI-tool.git
cd Top-AI-tool
```

### 2. Backend Setup (`agent-server`)

Navigate to the `agent-server` directory and install dependencies using `uv`:

```bash
cd agent-server
uv pip install -r requirements.txt
```

You will also need to install Playwright browsers:

```bash
playwright install
```

**Environment Variables**:
The Langchain agent currently uses `OpenAI` as a placeholder LLM. You will need to set your `OPENAI_API_KEY` environment variable for the agent to function correctly.

```bash
# For Windows
set OPENAI_API_KEY="your_openai_api_key_here"
# For Linux/macOS
export OPENAI_API_KEY="your_openai_api_key_here"
```

### 3. Frontend Setup (`web`)

Navigate to the `web` directory and install dependencies using `npm`:

```bash
cd web
npm install
```

## Usage

### 1. Start the Backend Server

From the `agent-server` directory:

```bash
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`.

### 2. Start the Frontend Application

From the `web` directory:

```bash
npm start
```

The React application will open in your browser, usually at `http://localhost:3000`.

### 3. Interact with the Application

*   Open your browser to `http://localhost:3000`.
*   Use the "Run AI Agent to Find Tools" section to enter a task (e.g., "Find top AI tools for natural language processing").
*   The agent will use the configured search engines to find information and store it in the SQLite database.
*   The "Collected AI Tools" section will automatically update with the new findings.

## Technologies Used

*   **Backend**: Python, FastAPI, Langchain, SQLite, Requests, BeautifulSoup, Playwright
*   **Frontend**: React, JavaScript, HTML, CSS
