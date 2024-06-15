// src/components/FileUpload.js
import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [library, setLibrary] = useState('spaCy');
  const [converter, setConverter] = useState('calibre');
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('library', library);
    formData.append('converter', converter);

    try {
      const response = await axios.post('http://127.0.0.1:8000/uploadfile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setResult(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h1>File Upload</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <select value={library} onChange={(e) => setLibrary(e.target.value)}>
          <option value="spaCy">spaCy</option>
          <option value="NLTK">NLTK</option>
          <option value="HFT">HFT</option>
        </select>
        <select value={converter} onChange={(e) => setConverter(e.target.value)}>
          <option value="calibre">Calibre</option>
          <option value="pandoc">Pandoc</option>
          <option value="unoconv">Unoconv</option>
          <option value="soffice">Soffice</option>
        </select>
        <button type="submit">Upload</button>
      </form>
      {result && (
        <div>
          <h2>Results</h2>
          <p>Filename: {result.filename}</p>
          <p>Conversion Time: {result.conversion_time} seconds</p>
          <p>Processing Time: {result.processing_time} seconds</p>
          <div>
            <h3>Entities:</h3>
            <pre>{JSON.stringify(result.entities, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
