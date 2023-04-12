import React, { useState } from 'react';
import './MyForm.css';

function MyForm() {
  const [textValue, setTextValue] = useState('');
  const [dropdownValue, setDropdownValue] = useState('');

  const handleTextChange = (event) => {
    setTextValue(event.target.value);
  }

  const handleDropdownChange = (event) => {
    setDropdownValue(event.target.value);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch("/api/my-endpoint", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ textValue, dropdownValue })
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Response from server:", data);
        // handle server response
      })
      .catch((error) => {
        console.error("Error sending request to server:", error);
        // handle error
      });
  };

  return (
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
          <option value="option1">SVM</option>
          <option value="option2">RNN</option>
          <option value="option3">Naive Bayes</option>
          <option value="option4">Bert BiLSTM</option>
        </select>
      </label>
        <br />
        <button type="submit">Submit Tweet</button>
      </form>
    </div>
  );
}

export default MyForm;
