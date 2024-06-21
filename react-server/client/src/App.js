import React, { useState } from 'react'
import './App.css'

function App() {
    const [input, setInput] = useState('')
    const [response, setResponse] = useState('')
    const [chatHistory, setChatHistory] = useState([]) // 2D array w/ structure [ ["Q1", "A1"], ..., ["Qn", "An"] ], where n is the total number of questions asked
    const [requestInProcess, setRequestInProcess] = useState(null)
    const [viewChatHistory, setViewChatHistory] = useState(false)

    const handleInputChange = (e) => {
        setInput(e.target.value)
    }

    const handleUserQuery = async (e) => {
      setRequestInProcess(true)
      // Sending the POST query to our backend Flask server
      try {
        const res = await fetch('http://127.0.0.1:5000/new_query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input }) 
        })
        const data = await res.json()
        setResponse(data.response)
        setChatHistory([...chatHistory, [input, data.response]])
        setInput('') // resetting input
      } catch (error) {
          console.error('Error:', error)
      }
      setRequestInProcess(false)
    }

    function toggleChatHistory() {
      setViewChatHistory(!viewChatHistory)
    }

    const convoHist = chatHistory.map((convo, index) =>
      <div className='q-and-a-wrapper' key={index}>
        <p><strong>Question</strong>: {convo[0]}</p>
        <p><strong>Answer</strong>: {convo[1]}</p>
      </div>
    )

    return (
        <div className='container'>
          <div className='form-wrapper'>
            <h1>User Query</h1>
            <form onSubmit={(e) => e.preventDefault()}>
              <textarea 
                value={input}
                onChange={handleInputChange}
                placeholder="Enter your query here..."
              ></textarea>
              <button type="button" onClick={handleUserQuery}>Run User Query</button>
            </form>
            <br /><hr /><br />
            {response ? (
                // We have a returned response
                requestInProcess ?
                  <p><strong>Response</strong>: TBD...</p>
                  : <p><strong>Response</strong>: {response}</p>
              ) : (  
                // We have no response. Is there a request being processed or not?
                requestInProcess ? 
                  <p><strong>Response</strong>: TBD...</p>
                  : <p><strong>Response</strong>: </p>
              )
            }
          </div>
          <br />
          <div className='chat-history-wrapper'>
            <div className='view-history-wrapper'>
              <h1>Chat History</h1>
              <button type="button" onClick={toggleChatHistory}>View</button>
            </div>
            {viewChatHistory && convoHist[0] && convoHist}
          </div>
        </div>
    )
}

export default App
