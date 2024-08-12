import { useState } from "react";
import "./App.css";

import { ReactTyped } from "react-typed";

import { Input } from "@chakra-ui/react";
import { Button } from "@chakra-ui/react";

function App() {
  const PORT = "5000";
  const ENDPOINT = "get_response";
  const URL = `http://127.0.0.1:${PORT}/${ENDPOINT}`;

  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [intraOutput, setIntraOutput] = useState(false);
  const [buttonDisabled, setButtonDisabled] = useState(false);

  function handleComplete() {
    setIntraOutput(false);
    setButtonDisabled(false);
  }

  async function getModelOutput() {
    console.log(intraOutput);

    if (intraOutput == true) {
      return;
    }

    setButtonDisabled(true);

    setIntraOutput(true);
    let modelOutput = await fetch(URL, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ input: input }),
    }).then((res) => res.json());

    setOutput(modelOutput);
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
            <Input
              className="search"
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter your question here"
            ></Input>
            {buttonDisabled == true ? null : (
              <Button
                onClick={() => getModelOutput()}
                disabled={buttonDisabled}
              >
                ➣
              </Button>
            )}
          </div>

          <div className="output">
            <ReactTyped
              onComplete={() => handleComplete()}
              typeSpeed={7}
              strings={[output]}
            />
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
