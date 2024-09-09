
import React, { useState } from 'react';
import axios from 'axios';
import { Form, Button, Container, Alert, Row, Col } from 'react-bootstrap';
import { AiFillCheckCircle, AiFillCloseCircle, AiOutlineClear } from 'react-icons/ai';
import { MdAgriculture } from 'react-icons/md';
import './App.css';


function App() {
    const [inputData, setInputData] = useState({
        nitrogen: '',
        phosphorus: '',
        potassium: '',
        temperature: '',
        humidity: '',
        ph_value: '',
        rainfall: ''
    });

    const [prediction, setPrediction] = useState(null);
    const [improvements, setImprovements] = useState([]);
    const [submitted, setSubmitted] = useState(false);

    // Handle input change
    const handleChange = (e) => {
        setInputData({
            ...inputData,
            [e.target.name]: e.target.value
        });
    };
    
    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitted(true);  // Mark as submitted for displaying results
        try {
            const response = await axios.post('https://cropupgrad.onrender.com/predict_crop', {
                Nitrogen: parseFloat(inputData.nitrogen),
                Phosphorus: parseFloat(inputData.phosphorus),
                Potassium: parseFloat(inputData.potassium),
                Temperature: parseFloat(inputData.temperature),
                Humidity: parseFloat(inputData.humidity),
                pH_Value: parseFloat(inputData.ph_value),
                Rainfall: parseFloat(inputData.rainfall)
            });

            console.log(response.data);  // Check the backend response
            setPrediction(response.data.predicted_crop);
            setImprovements(response.data.improvements || []);
        } catch (error) {
            console.error("There was an error making the request:", error);
        }
    };

    // Handle form clearing
    const handleClear = () => {
        setInputData({
            nitrogen: '',
            phosphorus: '',
            potassium: '',
            temperature: '',
            humidity: '',
            ph_value: '',
            rainfall: ''
        });
        setPrediction(null);
        setImprovements([]);
        setSubmitted(false);  // Clear submitted state
    };

    return (
        <Container className="mt-5">
            <h1 className="text-center mb-4">
                <MdAgriculture className="agri-icon" /> Crop Prediction and Improvement Suggestions
            </h1>

            <Form onSubmit={handleSubmit} className="form-container">
                <Row>
                    <Col md={6}>
                        <Form.Group controlId="nitrogen" className="mb-3">
                            <Form.Label>Nitrogen</Form.Label>
                            <Form.Control
                                type="number"
                                name="nitrogen"
                                value={inputData.nitrogen}
                                onChange={handleChange}
                                placeholder="Enter Nitrogen value"
                            />
                        </Form.Group>
                    </Col>
                    <Col md={6}>
                        <Form.Group controlId="phosphorus" className="mb-3">
                            <Form.Label>Phosphorus</Form.Label>
                            <Form.Control
                                type="number"
                                name="phosphorus"
                                value={inputData.phosphorus}
                                onChange={handleChange}
                                placeholder="Enter Phosphorus value"
                            />
                        </Form.Group>
                    </Col>
                </Row>
                <Row>
                    <Col md={6}>
                        <Form.Group controlId="potassium" className="mb-3">
                            <Form.Label>Potassium</Form.Label>
                            <Form.Control
                                type="number"
                                name="potassium"
                                value={inputData.potassium}
                                onChange={handleChange}
                                placeholder="Enter Potassium value"
                            />
                        </Form.Group>
                    </Col>
                    <Col md={6}>
                        <Form.Group controlId="temperature" className="mb-3">
                            <Form.Label>Temperature</Form.Label>
                            <Form.Control
                                type="number"
                                name="temperature"
                                value={inputData.temperature}
                                onChange={handleChange}
                                placeholder="Enter Temperature (°C)"
                            />
                        </Form.Group>
                    </Col>
                </Row>
                <Row>
                    <Col md={6}>
                        <Form.Group controlId="humidity" className="mb-3">
                            <Form.Label>Humidity</Form.Label>
                            <Form.Control
                                type="number"
                                name="humidity"
                                value={inputData.humidity}
                                onChange={handleChange}
                                placeholder="Enter Humidity (%)"
                            />
                        </Form.Group>
                    </Col>
                    <Col md={6}>
                        <Form.Group controlId="ph_value" className="mb-3">
                            <Form.Label>pH Value</Form.Label>
                            <Form.Control
                                type="number"
                                name="ph_value"
                                value={inputData.ph_value}
                                onChange={handleChange}
                                placeholder="Enter pH Value"
                            />
                        </Form.Group>
                    </Col>
                </Row>
                <Form.Group controlId="rainfall" className="mb-3">
                    <Form.Label>Rainfall</Form.Label>
                    <Form.Control
                        type="number"
                        name="rainfall"
                        value={inputData.rainfall}
                        onChange={handleChange}
                        placeholder="Enter Rainfall (mm)"
                    />
                </Form.Group>

                <div className="d-flex justify-content-between">
                    <Button variant="success" type="submit">
                        <AiFillCheckCircle className="btn-icon" /> Predict Crop
                    </Button>
                    <Button variant="danger" type="button" onClick={handleClear}>
                        <AiOutlineClear className="btn-icon" /> Clear Form
                    </Button>
                </div>
            </Form>

            {submitted && (
                <div className="results mt-5">
                    {prediction && (
                        <Alert variant="success">
                            <AiFillCheckCircle className="result-icon" /> 
                            <h4>Predicted Crop: {prediction}</h4>
                        </Alert>
                    )}
                    {improvements.length > 0 ? (
                        <Alert variant="info">
                            <AiFillCloseCircle className="result-icon" />
                            <h4>Suggested Improvements:</h4>
                            <ul>
                                {improvements.map((improvement, index) => (
                                    <li key={index}>{improvement}</li>
                                ))}
                            </ul>
                        </Alert>
                    ) : (
                        <Alert variant="warning">
                            <AiFillCloseCircle className="result-icon" /> 
                            <h4>No improvements needed for this crop.</h4>
                        </Alert>
                    )}
                </div>
            )}
        </Container>
    );
}

export default App;
