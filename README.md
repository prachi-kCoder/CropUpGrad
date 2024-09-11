
# CropUpGrad 🌱
CropUpGrad is an AI-powered tool designed to help farmers achieve better yields through data-driven insights.
App is live on: https://cropupgrad-clientside.onrender.com/

🌾 Crop Prediction: Analyze soil composition (Nitrogen, Humidity, Potassium, Rainfall) to recommend the best crops.
📈 Yield Improvement: Get actionable suggestions to enhance crop yield.
🌍 Sustainable Farming: Promote better farming practices with precise, data-backed recommendations.
Empower your farming with smarter decisions and sustainable practices using CropUpGrad!


![Crop_predictor_img](https://github.com/user-attachments/assets/a7d21656-bcee-446b-b206-3f49e59fc09e)
![Crop_predictor_image](https://github.com/user-attachments/assets/13f272bb-8e4f-4bbe-99f3-1d7790baf60e)


## Project Setup

This project includes both a server-side and client-side component. Follow the instructions below to set up the development environment for each part.

### Server-Side Setup

1. **Create a Virtual Environment**

   Navigate to the `server` directory and create a virtual environment using Python:

   ```bash
   cd server
   python -m venv improenv

2.Activate the Virtual Environment

  On Windows:
  
  (bash)
  improenv\Scripts\activate
  (On macOS/Linux)
  source improenv/bin/activate
  
3.Install Dependencies
  
  Install the necessary Python packages from requirements.txt:
  
  bash
  pip install -r requirements.txt
  
### Client-Side Setup
Navigate to the Client Directory

Move to the client directory, which contains the React application:

(bash)
cd client
Install Dependencies

Install the necessary Node.js packages using npm:

(bash)
npm install
(This will install all dependencies listed in package.json.)

#Running the Project
Server-Side: To start the server, ensure that your virtual environment is activated and then run your server application (e.g., uvicorn, gunicorn, or a similar command).

Client-Side: To start the React application, use:

bash
npm run dev
(This will start the development server provided by Vite.)
  
