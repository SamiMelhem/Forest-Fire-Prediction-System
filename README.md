# Forest-Fire-Prediction-System

## Core Functionalities
- Predict the likelihood that a US location will experience a wildfire within the next week (percentage chance).
- Provide a GUI that allows users to see a prediction zone (similar to a weather interface).

## Additional Features
- **Evacuation Routes** (TBD)
- **Notification System** (Requires DB persistence of user information)
- **Satellite Images** (Data collection for enhanced prediction)
- **Reinforcement Learning** (Enhance the prediction model over time)

---

## Steps
1. Data Collection
2. Model Training & Optimization
3. GUI Development
4. Backend API Development
5. Integration & Testing
6. Deployment

---

## Tech Stack

### Frontend (Web)
- Vite
- React
- Tailwind CSS

### Backend
- FastAPI

### APIs
- **Wildfire Data:** [Ambee](https://www.getambee.com/wildfire-api)

### AI/ML
- **Prediction Model:** (Depends on the dataset coming in)

### Database
- MongoDB Atlas

### Cloud & Infrastructure
- AWS (Arm-based server)
- Terraform
- Docker Containerization
- Extensions: Arm GitHub Extension

---

## Potential Datasets
- *(To be determined)*

---

## Resources
- [NASA Earth Data - Wildfires](https://www.earthdata.nasa.gov/topics/human-dimensions/wildfires)

---

## How to Run
### Prerequisites
- Node.js & npm (for frontend)
- Python (for backend with FastAPI)
- Docker (for containerization)
- MongoDB Atlas account

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/Forest-Fire-Prediction-System.git
   cd Forest-Fire-Prediction-System
   ```

2. Install dependencies for frontend and backend:
   ```sh
   cd frontend && npm install
   cd ../backend && pip install -r requirements.txt
   ```

3. Run the backend:
   ```sh
   uvicorn main:app --reload
   ```

4. Run the frontend:
   ```sh
   cd frontend
   npm run dev
   ```

5. Access the web app at `http://localhost:3000`

---

## Contributing
Feel free to contribute by submitting issues and pull requests!

---

## License
This project is licensed under the MIT License.
