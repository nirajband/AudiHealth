import React from 'react';
import '../styles/ResultsDisplay.css';

// Speech Milestone Data
const SPEECH_MILESTONES = {
  '0-3months': {
    age: '0-3 Months',
    milestones: [
      'Reacts to loud sounds',
      'Calms down or smiles when spoken to',
      'Recognizes your voice and calms down if crying',
      'Makes cooing sounds'
    ]
  },
  '4-6months': {
    age: '4-6 Months',
    milestones: [
      'Moves eyes in direction of sounds',
      'Responds to changes in tone of voice',
      'Notices toys that make sounds',
      'Babbling sounds more speech-like with many different sounds',
      'Laughs and giggles'
    ]
  },
  '7-12months': {
    age: '7-12 Months',
    milestones: [
      'Understands "no"',
      'Babbles with intonation (voice rises and falls)',
      'Says "mama" or "dada" without meaning',
      'Tries to communicate by actions or gestures',
      'Uses 1-2 words by first birthday'
    ]
  },
  '1-2years': {
    age: '1-2 Years',
    milestones: [
      'Points to a few body parts when asked',
      'Follows simple commands',
      'Understands simple questions ("Where\'s your shoe?")',
      'Uses many new words (vocabulary grows rapidly)',
      'Puts 2 words together ("more cookie", "no juice")',
      'Uses some one or two-word questions ("Where kitty?" "Go bye-bye?")'
    ]
  },
  '2-3years': {
    age: '2-3 Years',
    milestones: [
      'Understands differences in meaning ("go-stop", "big-little")',
      'Follows two-part directions',
      'Has a word for almost everything',
      'Uses 2-3 word sentences',
      'Speech becomes more accurate but may still mispronounce words',
      'Asks for or directs attention to objects by naming them'
    ]
  },
  '3-4years': {
    age: '3-4 Years',
    milestones: [
      'Hears you when you call from another room',
      'Hears television or radio at the same volume as other family members',
      'Answers simple "who?", "what?", "where?", "why?" questions',
      'Talks about activities at school or friends\' homes',
      'Uses sentences with 4 or more words',
      'Speaks easily without repeating syllables or words'
    ]
  },
  '4-5years': {
    age: '4-5 Years',
    milestones: [
      'Pays attention to a short story and answers questions',
      'Hears and understands most of what is said at home and school',
      'Uses sentences that give lots of details',
      'Tells stories that stick to topic',
      'Communicates easily with other children and adults',
      'Says most sounds correctly except a few like l, s, r, v, z, ch, sh, th',
      'Uses the same grammar as the rest of the family'
    ]
  }
};

// Child Speech Disorders Information
const SPEECH_DISORDERS = {
  'apraxia': {
    name: 'Childhood Apraxia of Speech (CAS)',
    description: 'A motor speech disorder where the child has difficulty planning and coordinating the movements needed for speech.',
    signs: [
      'Inconsistent errors in speech sounds',
      'Groping for sounds or difficulty moving from one sound to another',
      'Inconsistent voicing errors',
      'Difficulty with longer or more complex words'
    ],
    severity: {
      mild: 'May be difficult to understand 25-50% of the time',
      moderate: 'May be difficult to understand 50-75% of the time',
      severe: 'May be difficult to understand more than 75% of the time'
    }
  },
  'dysarthria': {
    name: 'Dysarthria',
    description: 'A motor speech disorder resulting from weakness or lack of coordination in speech muscles.',
    signs: [
      'Slurred or mumbled speech',
      'Speaking too slowly or too quickly',
      'Limited tongue, lip, and jaw movement',
      'Abnormal pitch and rhythm',
      'Changes in voice quality (hoarse, breathy, or nasal)'
    ],
    severity: {
      mild: 'Speech is understandable but may sound different',
      moderate: 'Speech is difficult to understand in some situations',
      severe: 'Speech is very difficult or impossible to understand'
    }
  },
  'stuttering': {
    name: 'Stuttering (Childhood-Onset Fluency Disorder)',
    description: 'A speech disorder characterized by disruptions in the flow of speech.',
    signs: [
      'Repetition of sounds, syllables, or words',
      'Prolongation of sounds',
      'Blocks (no sound)',
      'Physical tension while speaking',
      'Secondary behaviors (eye blinking, head nodding)'
    ],
    severity: {
      mild: 'Occasional stuttering, minimal impact on communication',
      moderate: 'Frequent stuttering, some avoidance of speaking situations',
      severe: 'Stuttering significantly impacts daily communication and quality of life'
    }
  },
  'phonological': {
    name: 'Phonological Disorder',
    description: 'Difficulty with the pattern of sounds in speech, affecting multiple sounds in a predictable way.',
    signs: [
      'Substituting one sound for another',
      'Omitting sounds in words',
      'Distorting sounds',
      'Adding extra sounds to words'
    ],
    severity: {
      mild: 'Affects 1-2 sound patterns, mostly intelligible',
      moderate: 'Affects multiple sound patterns, intelligibility reduced',
      severe: 'Affects many sound patterns, very difficult to understand'
    }
  },
  'language': {
    name: 'Language Delay/Disorder',
    description: 'Difficulty understanding or using spoken language appropriately for the child\'s age.',
    signs: [
      'Limited vocabulary for age',
      'Difficulty following directions',
      'Problems with sentence structure',
      'Difficulty expressing thoughts and ideas',
      'Trouble understanding others'
    ],
    severity: {
      mild: 'Slight delay, age-appropriate with support',
      moderate: 'Significant delay, requires speech therapy',
      severe: 'Profound delay, intensive intervention needed'
    }
  }
};

const ResultsDisplay = ({ result }) => {
  if (!result) return null;

  const isHealthy = result.prediction === 'Healthy';
  const severity = result.suggestion?.severity || 'moderate';

  return (
    <div className={`results-container ${isHealthy ? 'healthy' : 'unhealthy'}`}>
      <div className="results-header">
        <div className={`status-badge ${result.type}`}>
          {isHealthy ? '✓ Healthy Voice' : '⚠ Attention Needed'}
        </div>
        <h2 className="prediction-title">{result.prediction}</h2>
        <div className="confidence-meter">
          <span className="confidence-label">Confidence:</span>
          <div className="confidence-bar-container">
            <div 
              className="confidence-bar"
              style={{ width: `${result.confidence}%` }}
            />
          </div>
          <span className="confidence-value">{result.confidence}%</span>
        </div>
      </div>

      <div className="spectrogram-section">
        <h3>Voice Spectrogram</h3>
        <div className="spectrogram-container">
          <img 
            src={`http://localhost:5000${result.spectrogram}`}
            alt="Voice Spectrogram"
            className="spectrogram-image"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400"><rect width="800" height="400" fill="%23f0f0f0"/><text x="400" y="200" text-anchor="middle" fill="%23666" font-size="20">Spectrogram Loading...</text></svg>';
            }}
          />
        </div>
        <p className="spectrogram-description">
          This spectrogram shows the frequency content of your voice over time.
        </p>
      </div>

      {isHealthy ? (
        <HealthyMessage message={result.message} />
      ) : (
        <UnhealthyMessage 
          message={result.message}
          suggestion={result.suggestion}
          severity={severity}
        />
      )}

      <div className="results-footer">
        <small>Analysis performed on {new Date(result.timestamp).toLocaleString()}</small>
      </div>
    </div>
  );
};

const HealthyMessage = ({ message }) => (
  <div className="healthy-message">
    <div className="message-icon">🎉</div>
    <div className="message-content">
      <h3>Great News!</h3>
      <p className="main-message">{message}</p>
      <div className="tips-section">
        <h4>Keep Your Voice Healthy:</h4>
        <ul className="tips-list">
          <li>💧 Stay hydrated - drink plenty of water</li>
          <li>🗣️ Avoid shouting or straining your voice</li>
          <li>🚭 Stay away from smoke and pollutants</li>
          <li>😴 Get enough rest and sleep</li>
        </ul>
      </div>
    </div>
  </div>
);

const UnhealthyMessage = ({ message, suggestion, severity }) => {
  // Determine which milestones to show based on severity
  const getMilestonesToShow = () => {
    if (severity === 'severe') {
      return ['0-3months', '4-6months', '7-12months'];
    } else if (severity === 'moderate') {
      return ['1-2years', '2-3years', '3-4years'];
    } else {
      return ['3-4years', '4-5years'];
    }
  };

  const milestonesToShow = getMilestonesToShow();

  return (
    <div className="unhealthy-message">
      <div className="message-icon">⚠️</div>
      <div className="message-content">
        <h3>Medical Consultation Recommended</h3>
        <p className="main-message">{message}</p>
        
        {suggestion && (
          <div className="suggestion-card">
            <div className="severity-badge" data-severity={suggestion.severity}>
              {suggestion.severity.toUpperCase()}
            </div>
            
            <div className="suggestion-details">
              <h4>Recommendations:</h4>
              <p className="suggestion-text">{suggestion.suggestion}</p>
            </div>

            {suggestion.doctor_name && (
              <div className="doctor-info">
                <h4>Recommended Specialist:</h4>
                <div className="doctor-card">
                  <div className="doctor-icon">👨‍⚕️</div>
                  <div className="doctor-details">
                    <p className="doctor-name">{suggestion.doctor_name}</p>
                    <p className="doctor-spec">{suggestion.specialization}</p>
                    <p className="doctor-contact">{suggestion.contact}</p>
                  </div>
                </div>
              </div>
            )}

            {/* SPEECH MILESTONES SECTION - REPLACES IMMEDIATE ACTIONS */}
            <div className="speech-milestones-section">
              <h4>📊 Speech Development Milestones</h4>
              <p className="milestone-intro">
                Children with {severity} speech concerns should be monitored for these developmental milestones:
              </p>
              
              {milestonesToShow.map((key) => {
                const milestone = SPEECH_MILESTONES[key];
                return (
                  <div key={key} className="milestone-card">
                    <h5 className="milestone-age">{milestone.age}</h5>
                    <ul className="milestone-list">
                      {milestone.milestones.map((item, index) => (
                        <li key={index}>✓ {item}</li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>

            {/* COMMON SPEECH DISORDERS SECTION */}
            <div className="speech-disorders-section">
              <h4>🔍 Common Childhood Speech Disorders</h4>
              <p className="disorders-intro">
                Understanding common speech disorders can help in early identification and intervention:
              </p>
              
              <div className="disorders-grid">
                {Object.entries(SPEECH_DISORDERS).map(([key, disorder]) => (
                  <div key={key} className="disorder-card">
                    <h5 className="disorder-name">{disorder.name}</h5>
                    <p className="disorder-description">{disorder.description}</p>
                    
                    <div className="disorder-signs">
                      <strong>Common Signs:</strong>
                      <ul>
                        {disorder.signs.slice(0, 3).map((sign, index) => (
                          <li key={index}>{sign}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="disorder-severity">
                      <strong>Severity Indicators:</strong>
                      <div className="severity-info">
                        <span className="severity-label mild">Mild:</span>
                        <span className="severity-desc">{disorder.severity.mild}</span>
                      </div>
                      <div className="severity-info">
                        <span className="severity-label moderate">Moderate:</span>
                        <span className="severity-desc">{disorder.severity.moderate}</span>
                      </div>
                      <div className="severity-info">
                        <span className="severity-label severe">Severe:</span>
                        <span className="severity-desc">{disorder.severity.severe}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="warning-box">
          <strong>⚠️ Important:</strong> This is an AI-assisted preliminary analysis. 
          Please consult with a qualified healthcare professional for proper diagnosis and treatment.
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;


// import "../styles/ResultsDisplay.css"

// const ResultsDisplay = ({ result }) => {
//   if (!result) return null

//   const isHealthy = result.prediction === "Healthy"

//   return (
//     <div className={`results-container ${isHealthy ? "healthy" : "unhealthy"}`}>
//       <div className="results-header">
//         <div className={`status-badge ${result.type}`}>{isHealthy ? "✓ Healthy Voice" : "⚠ Attention Needed"}</div>
//         <h2 className="prediction-title">{result.prediction}</h2>
//         <div className="confidence-meter">
//           <span className="confidence-label">Confidence:</span>
//           <div className="confidence-bar-container">
//             <div className="confidence-bar" style={{ width: `${result.confidence}%` }} />
//           </div>
//           <span className="confidence-value">{result.confidence}%</span>
//         </div>
//       </div>

//       <div className="spectrogram-section">
//         <h3>Voice Spectrogram</h3>
//         <div className="spectrogram-container">
//           <img
//             src={`http://localhost:5000${result.spectrogram}`}
//             alt="Voice Spectrogram"
//             className="spectrogram-image"
//             onError={(e) => {
//               e.target.onerror = null
//               e.target.src =
//                 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400"><rect width="800" height="400" fill="%23f0f0f0"/><text x="400" y="200" text-anchor="middle" fill="%23666" font-size="20">Spectrogram Loading...</text></svg>'
//             }}
//           />
//         </div>
//         <p className="spectrogram-description">This spectrogram shows the frequency content of your voice over time.</p>
//       </div>

//       {isHealthy ? (
//         <HealthyMessage message={result.message} />
//       ) : (
//         <UnhealthyMessage message={result.message} suggestion={result.suggestion} />
//       )}

//       <div className="results-footer">
//         <small>Analysis performed on {new Date(result.timestamp).toLocaleString()}</small>
//       </div>
//     </div>
//   )
// }

// const HealthyMessage = ({ message }) => (
//   <div className="healthy-message">
//     <div className="message-icon">🎉</div>
//     <div className="message-content">
//       <h3>Great News!</h3>
//       <p className="main-message">{message}</p>
//       <div className="tips-section">
//         <h4>Keep Your Voice Healthy:</h4>
//         <ul className="tips-list">
//           <li>💧 Stay hydrated - drink plenty of water</li>
//           <li>🗣️ Avoid shouting or straining your voice</li>
//           <li>🚭 Stay away from smoke and pollutants</li>
//           <li>😴 Get enough rest and sleep</li>
//         </ul>
//       </div>
//     </div>
//   </div>
// )

// const UnhealthyMessage = ({ message, suggestion }) => (
//   <div className="unhealthy-message">
//     <div className="message-icon">⚠️</div>
//     <div className="message-content">
//       <h3>Medical Consultation Recommended</h3>
//       <p className="main-message">{message}</p>

//       {suggestion && (
//         <div className="suggestion-card">
//           <div className="severity-badge" data-severity={suggestion.severity}>
//             {suggestion.severity.toUpperCase()}
//           </div>

//           <div className="suggestion-details">
//             <h4>Recommendations:</h4>
//             <p className="suggestion-text">{suggestion.suggestion}</p>
//           </div>

//           {suggestion.doctor_name && (
//             <div className="doctor-info">
//               <h4>Recommended Specialist:</h4>
//               <div className="doctor-card">
//                 <div className="doctor-icon">👨‍⚕️</div>
//                 <div className="doctor-details">
//                   <p className="doctor-name">{suggestion.doctor_name}</p>
//                   <p className="doctor-spec">{suggestion.specialization}</p>
//                   <p className="doctor-contact">{suggestion.contact}</p>
//                 </div>
//               </div>
//             </div>
//           )}

//           <div className="immediate-actions">
//             <h4>Immediate Actions:</h4>
//             <ul className="action-list">
//               <li>🔇 Rest your voice completely</li>
//               <li>💧 Drink warm water</li>
//               <li>🌡️ Use a humidifier</li>
//               <li>📞 Schedule medical consultation</li>
//             </ul>
//           </div>
//         </div>
//       )}

//       <div className="warning-box">
//         <strong>⚠️ Important:</strong> This is an AI-assisted preliminary analysis. Please consult with a qualified
//         healthcare professional for proper diagnosis.
//       </div>
//     </div>
//   </div>
// )

// export default ResultsDisplay

