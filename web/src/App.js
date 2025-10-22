import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [agentTask, setAgentTask] = useState('');
  const [agentResponse, setAgentResponse] = useState('');
  const [submittingAgentTask, setSubmittingAgentTask] = useState(false);

  const fetchTools = async () => {
    try {
      const response = await fetch('http://localhost:8000/tools');
      const data = await response.json();
      setTools(data);
    } catch (error) {
      console.error('Error fetching AI tools:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTools();
  }, []);

  const handleAgentTaskSubmit = async (e) => {
    e.preventDefault();
    setSubmittingAgentTask(true);
    setAgentResponse('Running agent...');
    try {
      const response = await fetch('http://localhost:8000/run_agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task: agentTask }),
      });
      const data = await response.json();
      setAgentResponse(JSON.stringify(data, null, 2));
      setAgentTask('');
      fetchTools(); // Refresh tools after agent runs
    } catch (error) {
      console.error('Error running agent:', error);
      setAgentResponse(`Error: ${error.message}`);
    } finally {
      setSubmittingAgentTask(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Top AI Tools Dashboard</h1>
      </header>
      <main>
        <section className="agent-section">
          <h2>Run AI Agent to Find Tools</h2>
          <form onSubmit={handleAgentTaskSubmit}>
            <textarea
              value={agentTask}
              onChange={(e) => setAgentTask(e.target.value)}
              placeholder="e.g., Find the latest AI tools for image generation"
              rows="4"
              cols="50"
              disabled={submittingAgentTask}
            ></textarea>
            <br />
            <button type="submit" disabled={submittingAgentTask}>
              {submittingAgentTask ? 'Running...' : 'Run Agent'}
            </button>
          </form>
          {agentResponse && (
            <div className="agent-response">
              <h3>Agent Output:</h3>
              <pre>{agentResponse}</pre>
            </div>
          )}
        </section>

        <section className="tools-list-section">
          <h2>Collected AI Tools</h2>
          {loading ? (
            <p>Loading tools...</p>
          ) : (
            <div className="tools-grid">
              {tools.length === 0 ? (
                <p>No AI tools collected yet. Run the agent to find some!</p>
              ) : (
                tools.map((tool, index) => (
                  <div key={index} className="tool-card">
                    <h3>{tool.name}</h3>
                    <p>{tool.description}</p>
                    {tool.url && <p><a href={tool.url} target="_blank" rel="noopener noreferrer">{tool.url}</a></p>}
                    {tool.source && <p>Source: {tool.source}</p>}
                    {tool.search_query && <p>Search Query: {tool.search_query}</p>}
                  </div>
                ))
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
