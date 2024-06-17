import React, { useState } from 'react';
import './App.css';

function App() {
    const [input, setInput] = useState('');
    const [response, setResponse] = useState('');
    const [requestInProcess, setRequestInProcess] = useState(null)

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

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
        });
        const data = await res.json();
        console.log('Response: ', data.response)
        setResponse(data.response);
      } catch (error) {
          console.error('Error:', error);
      }
      setRequestInProcess(false)
    }

    const getCurrentData = async (e) => {   
      setRequestInProcess(true)     
      // Sending the GET query to our backend Flask server
      try {
          const res = await fetch('http://127.0.0.1:5000/get_existing_data', {
              method: 'GET',
              headers: {
                  'Content-Type': 'application/json'
              }
          });
          const data = await res.json();
          console.log('Response: ', data.members)
          setResponse(data.members);
      } catch (error) {
          console.error('Error:', error);
      }
      setRequestInProcess(false)
    };

    return (
        <div className='container'>
          <div className='form-wrapper'>
            <form onSubmit={(e) => e.preventDefault()}>
              <textarea 
                value={input}
                onChange={handleInputChange}
                placeholder="Enter your text here..."
              ></textarea>
              <button type="button" onClick={handleUserQuery}>Run User Query</button>
              <br />
              <button type="button" onClick={getCurrentData}>Get Current Data</button>
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
        </div>
    );
}

export default App;