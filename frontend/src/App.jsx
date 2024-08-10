import { useState } from 'react'
import './App.css'

import { ReactTyped } from "react-typed";

import { Input } from '@chakra-ui/react'
import { Button } from '@chakra-ui/react'

function App() {

  const PORT = "5000"
  const ENDPOINT = "/get_response";
  const URL = `http://127.0.0.1:${PORT}/${ENDPOINT}`;

  const [output,setOutput] = useState("");
  const [intraOutput,setIntraOutput] = useState(false);

  function getModelOutput(input) {

  }

  function getOutput() {
    if (intraOutput == true) {
      return;
    }
    setIntraOutput(true)
    console.log("Received Output!");
    setOutput("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
  }

  return (
    <>
    <div>

      <div className="title">
        <span className="dune">Dune</span>
        <span className="gpt">GPT</span>
      </div>

      <div className="search-output-container">

        <div className="search-button-container">
          <Input className="search" placeholder="Enter your question here"></Input>
          <Button onClick={getOutput}>➣</Button>
        </div>
        

        <div className="output">
          <ReactTyped onComplete={() => setIntraOutput(false)} typeSpeed={7} strings={[output]}/>
        </div>
      </div>

      

    </div>
    </>
  )
}

export default App
