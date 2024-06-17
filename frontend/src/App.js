import './App.css';
import React, { useState} from 'react';
import axios from 'axios';

function App() {

  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState({started: false, pc: 0});
  const [msg, setMsg] = useState(null);
  const [selectedId, setSelectedId] = useState('spaCy');



  function handleLibrary(event){
    setSelectedId(event.target.value);
  }

  function handleChange(event) {
    setFile(event.target.files[0]);
  }
  
  function handleSubmit() {
    
    if (!file){
      setMsg("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append('file', file, file.name);
    const url = 'http://localhost:3000/post';
  
    const config = {
      headers: {
        'Custom-Header': 'value',
        // "Content-Type": "multipart/form-data; charset=utf-8;"
      }
    };

    setMsg("Uploading...");
    setProgress(prevState =>{
      return {...prevState, started: true}
    })
    axios.post(url, formData, {
      onUploadProgress: (progressEvent) => {
        setProgress(prevState => {
          return {...prevState, pc: progressEvent.progress*100}
        })},
        config
    })
      .then((response) => {
        setMsg("Upload successful");
        console.log(response.data);
      })
      .catch((error) => {
        setMsg("Upload Failed");
        console.error(error);
      });
  }

  return (
    <div className="App">
      <form method="post">
        <div className="header">
          <div className="head">
            <div className="box">
              <div><h3>Upload File To Your Library</h3></div>
              <div className="input"><label>Please select a library and choose a file to upload</label></div>
              <div className="lib">
              <div>
                <label >Choose a library: </label>
                <select onChange={handleLibrary} className= "library" name="library">
                  <option value="spaCy">spaCy</option>
                  <option value="NLTK">NLTK</option>
                  <option value="HFT">HFT</option>
                </select>
                </div>
                <span>Choose a file: </span>
                <input className="file" type="file"onChange={handleChange}/>
                <button className="submit" type="submit" onClick={handleSubmit}>Upload</button>
              </div>
            </div>
          </div>
        </div>
      </form>
      {progress.started && <progress max="100" value={progress.pc}></progress>}
      {msg && <span>{msg}</span>}
    </div>
  );
}

export default App;
