"use client"

import { useState } from "react"
import ResultsDisplay from "./ResultsDisplay"
import "../styles/Audichecker.css"

function Audichecker() {
  const [audioFile, setAudioFile] = useState(null)
  const [audioURL, setAudioURL] = useState(null)
  const [diagnosisResult, setDiagnosisResult] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (file && file.name.endsWith(".wav")) {
      setAudioFile(file)
      setAudioURL(URL.createObjectURL(file))
      setDiagnosisResult(null)
    } else {
      alert("Please upload a .wav file")
    }
  }

  const handleDiagnose = async () => {
    if (!audioFile) {
      alert("Please upload an audio file first!")
      return
    }

    setIsAnalyzing(true)
    setDiagnosisResult(null)

    const formData = new FormData()
    formData.append("audio", audioFile)

    try {
      const response = await fetch("http://localhost:5000/api/diagnose", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()
      setDiagnosisResult(data)
    } catch (error) {
      console.error("Error:", error)
      alert(`Failed to analyze: ${error.message}`)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="audichecker-container">
      <div className="upload-section">
        <h1>🎤 Voice Pathology Detection</h1>

        <div className="file-upload-area">
          <input type="file" accept=".wav" onChange={handleFileUpload} id="audio-input" style={{ display: "none" }} />
          <label htmlFor="audio-input" className="upload-label">
            📁 Choose WAV File
          </label>
        </div>

        {audioFile && (
          <div className="file-preview">
            <p>📄 Uploaded: {audioFile.name}</p>
            {audioURL && (
              <audio controls src={audioURL}>
                Your browser does not support audio.
              </audio>
            )}
          </div>
        )}

        <button onClick={handleDiagnose} disabled={!audioFile || isAnalyzing} className="diagnose-button">
          {isAnalyzing ? "⏳ Analyzing..." : "🔍 Diagnose Voice"}
        </button>
      </div>

      {isAnalyzing && (
        <div className="loading-section">
          <div className="spinner"></div>
          <p>Analyzing your voice... Please wait</p>
        </div>
      )}

      {diagnosisResult && (
        <div className="results-section">
          <h2>Diagnosis Results:</h2>
          <ResultsDisplay result={diagnosisResult} />
        </div>
      )}
    </div>
  )
}

export default Audichecker



// import React, { useState } from 'react';
// import ResultsDisplay from './ResultsDisplay';
// import '../styles/Audichecker.css';

// function Audichecker() {
//   const [audioFile, setAudioFile] = useState(null);
//   const [audioURL, setAudioURL] = useState(null);
//   const [diagnosisResult, setDiagnosisResult] = useState(null);
//   const [isAnalyzing, setIsAnalyzing] = useState(false);

//   const handleFileUpload = (event) => {
//     const file = event.target.files[0];
//     if (file && file.name.endsWith('.wav')) {
//       setAudioFile(file);
//       setAudioURL(URL.createObjectURL(file));
//       setDiagnosisResult(null);
//     } else {
//       alert('Please upload a .wav file');
//     }
//   };

//   const handleDiagnose = async () => {
//     if (!audioFile) {
//       alert('Please upload an audio file first!');
//       return;
//     }

//     setIsAnalyzing(true);
//     setDiagnosisResult(null);

//     const formData = new FormData();
//     formData.append('audio', audioFile);

//     try {
//       const response = await fetch('http://localhost:5000/api/diagnose', {
//         method: 'POST',
//         body: formData,
//       });

//       if (!response.ok) {
//         throw new Error(`Server error: ${response.status}`);
//       }

//       const data = await response.json();
//       setDiagnosisResult(data);
      
//     } catch (error) {
//       console.error('Error:', error);
//       alert(`Failed to analyze: ${error.message}`);
//     } finally {
//       setIsAnalyzing(false);
//     }
//   };

//   return (
//     <div className="audichecker-container">
//       <div className="upload-section">
//         <h1>Voice Pathology Detection</h1>
        
//         <div className="file-upload-area">
//           <input 
//             type="file" 
//             accept=".wav"
//             onChange={handleFileUpload}
//             id="audio-input"
//             style={{ display: 'none' }}
//           />
//           <label htmlFor="audio-input" className="upload-label">
//             📁 Choose WAV File
//           </label>
//         </div>

//         {audioFile && (
//           <div className="file-preview">
//             <p>📄 Uploaded: {audioFile.name}</p>
//             {audioURL && (
//               <audio controls src={audioURL} style={{ width: '100%', marginTop: '10px' }}>
//                 Your browser does not support audio.
//               </audio>
//             )}
//           </div>
//         )}

//         <button 
//           onClick={handleDiagnose} 
//           disabled={!audioFile || isAnalyzing}
//           className="diagnose-button"
//         >
//           {isAnalyzing ? '⏳ Analyzing...' : '🔍 Diagnose Voice'}
//         </button>
//       </div>

//       {isAnalyzing && (
//         <div className="loading-section">
//           <div className="spinner"></div>
//           <p>Analyzing your voice... Please wait</p>
//         </div>
//       )}

//       {diagnosisResult && (
//         <div className="results-section">
//           <h2>Diagnosis Results:</h2>
//           <ResultsDisplay result={diagnosisResult} />
//         </div>
//       )}
//     </div>
//   );
// }

// export default Audichecker;