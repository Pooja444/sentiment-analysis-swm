import React, { useState } from 'react';
import './MyForm.css';

function MyForm() {
  const [textValue, setTextValue] = useState('');
  const [dropdownValue, setDropdownValue] = useState('SVM');
  const [sentiment, setSentiment] = useState('');
  const [confidenceScore, setConfidenceScore] = useState('')

  const handleTextChange = (event) => {
    setTextValue(event.target.value);
  }

  const handleDropdownChange = (event) => {
    setDropdownValue(event.target.value);
    console.log(dropdownValue)
  }

  const handleSubmit = (event) => {
    console.log("Submitting tweet")
    event.preventDefault();
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(
        {
          tweet: textValue,
          model: dropdownValue
        }
      )
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Response from server:", data);
        // handle server response
        setSentiment(data.sentiment)
        setConfidenceScore(data.confidence_score)
      })
      .catch((error) => {
        console.error("Error sending request to server:", error);
        // handle error
      });
  };

  return (
    <div>
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <label>
            Enter Tweet:
            <input type="text" value={textValue} onChange={handleTextChange} />
          </label>
          <br />
          <label>
            Select the Machine Learning Model:
            <select value={dropdownValue} onChange={handleDropdownChange}>
              <option value="SVM">SVM</option>
              <option value="RNN">RNN</option>
              <option value="Naive Bayes">Naive Bayes</option>
              <option value="Bert BiLSTM">Bert BiLSTM</option>
            </select>
          </label>
          <br />
          <button type="submit">Submit Tweet</button>
        </form>
      </div>
      <div className="sentiment">
        Sentiment: {sentiment}
      </div>
      <div className="sentiment">
        Confidence Score: {confidenceScore}
      </div>
    </div>
  );
}

export default MyForm;
