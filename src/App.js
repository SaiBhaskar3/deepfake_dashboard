import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Navbar, Nav, Container, Form, Button, Card } from 'react-bootstrap';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import './App.css';
import axios from 'axios';

function App() {
  const [confidence, setConfidence] = useState(null);
  const [reportUrl, setReportUrl] = useState('');
  const [file, setFile] = useState(null);
  const [label, setLabel] = useState('');

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setConfidence(response.data.confidence / 100);  // scale to 0-1
      setLabel(response.data.label);
      setReportUrl(`http://127.0.0.1:5000${response.data.report_url}`);
    } catch (err) {
      console.error('Upload failed:', err);
      alert('Error analyzing file');
    }
  };

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand>Deepfake Detection</Navbar.Brand>
          <Nav className="ms-auto">
            <Nav.Link href="#">History</Nav.Link>
            <Nav.Link href="#">Logout</Nav.Link>
          </Nav>
        </Container>
      </Navbar>

      <Container className="mt-5">
        <h2 className="text-center mb-4">Deepfake Detection Dashboard</h2>

        <Card className="p-4 shadow-sm">
          <Form>
            <Form.Group className="mb-3">
              <Form.Label><strong>Upload Media</strong></Form.Label>
              <Form.Control type="file" onChange={(e) => setFile(e.target.files[0])} />
            </Form.Group>

            <Button onClick={handleUpload} className="w-100 mb-4" variant="primary">
              Analyze
            </Button>
          </Form>

          {confidence !== null && (
            <>
              <h5 className="text-center">Detection Summary</h5>
              <div className="d-flex justify-content-center" style={{ width: 200, margin: 'auto' }}>
                <CircularProgressbar
                  value={confidence * 100}
                  text={`${(confidence * 100).toFixed(1)}%`}
                  styles={buildStyles({
                    textColor: "#000",
                    pathColor: label === "Fake" ? "#ff0000" : "#00cc00",
                    trailColor: "#eee",
                  })}
                />
              </div>
              <div className="text-center mt-3">
                <strong>{(confidence * 100).toFixed(1)}% {label}</strong><br />
                <a href={reportUrl} target="_blank" rel="noopener noreferrer" download>
                  📄 Download Report
                </a>
              </div>
            </>
          )}
        </Card>
      </Container>
    </>
  );
}

export default App;
