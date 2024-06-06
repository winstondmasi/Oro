import logo from './logo.svg';
import './App.css';
import './index.css';
import React from 'react';

function App(){

    return(
      <>
        <div className="grid grid-cols-1 gap-4 p-8 bg-gray-900 text-white">
          <div className="grid grid-cols-[300px_1fr_300px] gap-4">
            <div className="bg-gray-800 rounded-lg p-6 flex flex-col gap-4">
              <div className="text-2xl font-bold">Youtube Summarize</div>
              <input
                type="text"
                placeholder="Enter YouTube URL"
                className="bg-gray-700 border-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div className="bg-gray-800 rounded-lg p-6 flex flex-col gap-4 justify-center items-center">
              <div className="text-2xl font-bold">Flash cards to download here</div>
            </div>
            <div />
          </div>
          <div className="bg-gray-800 rounded-lg p-6 flex flex-col gap-4 flex-1 h-[500px]">
            <div className="text-2xl font-bold">Summary will appear here</div>
            <p className="text-gray-400">
              This is a longer summary that will take up more vertical space. It will provide more details and information
              about the YouTube video that was summarized.
            </p>
            <p className="text-gray-400">
              Additional details and insights can be added here to make the summary more comprehensive and informative for
              the user.
            </p>
            <p className="text-gray-400">
              The summary can include key points, important quotes, and a high-level overview of the video's content.
            </p>
          </div>
        </div>
      </>
    );
}

export default App;
