import logo from './logo.svg';
import './App.css';
import './index.css';
import React, { useState } from 'react';
import axios from 'axios';


function App(){

  const[input, setInput] = useState('');
  const[summary, setSummary] = useState('');

  // handle summary submission
  const handleSubmit = async (event) =>{
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/backend/video_id', { video_id: input ,  request_type: 'summary'});
      setSummary(response.data.response);
    } catch (error) {
      console.error('Error fetching summarized data:', error);
    }
  }

  // handle flashcard generation
  const handleGenerateFlashcards = async (event) =>{
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/backend/video_id', { video_id: input ,  request_type: 'flashcards'}, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob[response.data])
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'flashcards.apkg');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('Error fetching flashcards data:', error);
    }
  }
  

  return(
    <>
      <div className="grid grid-cols-1 gap-4 p-8 bg-gray-900 text-white">
        <div className="grid grid-cols-[300px_1fr_300px] gap-4">
          <div className="bg-gray-800 rounded-lg p-6 flex flex-col gap-4 min-w-[350px]">
            <div className="text-3xl font-bold">YouTube Summarize</div>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Enter YouTube URL"
                className="bg-gray-700 border-none focus:ring-2 focus:ring-primary w-[400px]"
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <button className="bg-primary hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={handleSubmit}>⏎</button>
            </div>
            <div className="text-gray-400">
              Note: Don't enter full url
              <br />
              <br /> DON'T: https://www.youtube.com/watch?v=9bZkp7q19f0
              <br /> 
              <br /> DO: 9bZkp7q19f0
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 flex flex-col gap-4 justify-center items-center ml-20">
            <button className="bg-purple hover:bg-purple-700 text-white text-2xl font-bold py-2 px-4 rounded" onClick={handleGenerateFlashcards}>
              Flash cards to Download here
            </button>
          </div>
          <div />
        </div>
        <div className="bg-gray-800 rounded-lg p-6 flex flex-col gap-4 flex-1 h-[1200px]">
          <div className="text-2xl font-bold">Summary will appear here</div>
          {!summary && (
            <p className="text-gray-400">
              This is a longer summary that will take up more vertical space. It will provide more details and information
              about the YouTube video that was summarized.<br /><br />

              Additional details and insights can be added here to make the summary more comprehensive and informative for
              the user. <br /><br />

              The summary can include key points, important quotes, and a high-level overview of the video's content.
            </p>
          )}
          { summary && <p>{summary}</p>} {/* display the summary if it exists */}
        </div>
      </div>
    </>
  );
}

export default App;
