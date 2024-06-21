import React, { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
    const [input, setInput] = useState('')
    const [chatHistory, setChatHistory] = useState([]) // 2D array w/ structure [ ["Q1", "A1"], ..., ["Qn", "An"] ], where n is the total number of questions asked
    const [requestInProcess, setRequestInProcess] = useState(null)

    const messagesEndRef = useRef(null) // Ref to the last message element

    // Function to scroll to the bottom of chat history
    const scrollToBottom = () => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
        }
    }

    // Effect to scroll to bottom whenever chatHistory changes
    useEffect(() => {
        scrollToBottom()
    }, [chatHistory])

    const handleInputChange = (e) => {
        setInput(e.target.value)
    }

    const handleKeyDown = (e) => {
      if (e.key === 'Enter') handleUserQuery()
    }

    const handleUserQuery = async (e) => {
      setRequestInProcess(true)

      const userMessage = input.trim()
      if (!userMessage) return
      setInput("") // resetting input

      // Update chat history with user's message
      setChatHistory(prev => [...prev, { text: userMessage, isUser: true }])

      // Sending the POST query to our backend Flask server
      try {
        // Simulating backend response delay
        await new Promise(resolve => setTimeout(resolve, 1000))

        const res = await fetch('http://127.0.0.1:5000/new_query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input }) 
        })
        const data = await res.json()
        setChatHistory(prev => [...prev, { text: data.response, isUser: false }])
      } catch (error) {
          console.error('Error:', error)
      }
      setRequestInProcess(false)
    }

    // TODO: Store conversation history into SQLite and display it in a side bar so the user can go back to any conversation
    const convoHist = chatHistory.map((convo, index) =>
      <div className={convo.isUser ? 'message user-message' : 'message response-message'} key={index} ref={messagesEndRef}>
        {convo.text}
      </div>
    )

    return (
      <div className="container">
        <h1>RAG Chatbot</h1>
        <div className="chat-history-wrapper">
          {convoHist[0] && convoHist}
          {requestInProcess && (
              <div className="message response-message">Loading...</div>
          )}
        </div>
        <div className="form-wrapper">
          <input
              type="text"
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Enter your message..."
          />
          <button onClick={handleUserQuery} disabled={!input || requestInProcess}>
              Send
          </button>
        </div>
      </div>
    )
}

export default App
