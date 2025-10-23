import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [agentTask, setAgentTask] = useState('');
  const [agentResponse, setAgentResponse] = useState('');
  const [submittingAgentTask, setSubmittingAgentTask] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [limit, setLimit] = useState(20);

  const fetchTools = async (search = '', toolLimit = limit) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (toolLimit) params.append('limit', toolLimit);
      
      const response = await fetch(`http://localhost:8000/tools?${params}`);
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
          
          {/* Search and Filter Controls */}
          <div className="tools-controls">
            <div className="search-box">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search tools by name or description..."
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    fetchTools(searchTerm, limit);
                  }
                }}
              />
              <button onClick={() => fetchTools(searchTerm, limit)}>Search</button>
              {searchTerm && (
                <button 
                  onClick={() => {
                    setSearchTerm('');
                    fetchTools('', limit);
                  }}
                  className="clear-btn"
                >
                  Clear
                </button>
              )}
            </div>
            
            <div className="limit-selector">
              <label>Show: </label>
              <select
                value={limit}
                onChange={(e) => {
                  const newLimit = parseInt(e.target.value);
                  setLimit(newLimit);
                  fetchTools(searchTerm, newLimit);
                }}
              >
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>
            </div>
          </div>

          {loading ? (
            <p>Loading tools...</p>
          ) : (
            <div className="tools-container">
              <div className="tools-stats">
                <p>Found {tools.length} tool{tools.length !== 1 ? 's' : ''}</p>
              </div>
              <div className="tools-grid">
                {tools.length === 0 ? (
                  <p>No AI tools found. {searchTerm ? 'Try a different search term.' : 'Run the agent to find some!'}</p>
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
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
