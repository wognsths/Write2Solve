# Write2Solve - Math Equation OCR and Solution Verification Tool

## Project Overview
Write2Solve is an application that recognizes handwritten math equations, converts them into LaTeX format, and verifies the solutions provided by users. It utilizes OCR (Optical Character Recognition) technology and OpenAI's o3-mini model to ensure accurate equation recognition and solution verification.

## Key Features
1. **Capture and Save Equation Images**: Users can take pictures of handwritten math equations and upload them, which will be saved with a unique ID.
2. **OCR for Equation Recognition**: The uploaded images are processed to recognize math equations and convert them into LaTeX format.
3. **Equation Editing**: Users can directly modify the recognized equations.
4. **Solution Verification**: Users can verify their solutions through two methods:
   - Automatic verification based on OCR-recognized equations.
   - Verification based on user-provided problem descriptions (prompts).

## System Architecture
- **Frontend**: Provides the user interface.
- **Backend**: REST API based on FastAPI.
  - OCR Service: Recognizes equations from images.
  - LaTeX Service: Renders and verifies equations.
  - Storage Service: Manages images, equations, and solution data.
  - Reasoning Service: Utilizes OpenAI's o3-mini model for solution verification.

## Installation and Execution

### Prerequisites
- Docker and Docker Compose
- OpenAI API Key (for using the o3-mini model)

### Environment Setup
1. Clone the project
   ```bash
   git clone https://github.com/yourusername/Write2Solve.git
   cd Write2Solve
   ```

2. Set up environment variables
   - Create a `.env` file and add the following content:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running the Application
1. Run using Docker Compose
   ```bash
   docker-compose up -d
   ```

2. Access via browser
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## API Endpoints
- `POST /api/v1/ocr/`: Upload image and process OCR
- `GET /api/v1/equations/{equation_id}`: Retrieve saved equation
- `PUT /api/v1/equations/{equation_id}`: Update equation
- `POST /api/v1/solutions/`: Save and verify solution
- `POST /api/v1/verify/`: Verify solution based on OCR-recognized equation
- `POST /api/v1/verify-with-prompt/`: Verify solution based on user input prompt

## Data Storage Structure
- `data/images/`: Store uploaded images
- `data/equations/`: Store recognized equations
- `data/solutions/`: Store user solutions
- `data/corrections/`: Store data for improving the OCR model

## User Scenario Examples
1. **Verification of OCR-recognized Equations**:
   - Upload equation image → OCR recognition → Obtain equation ID → Submit solution → Check verification results
   
2. **Custom Prompt Verification**:
   - Write problem description (e.g., "Please solve the equation x^2 + 2x + 1 = 0") → Submit solution → Check verification results

## License
MIT License