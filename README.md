# Virtual Advisor

Virtual Advisor is a chatbot application built using Flask for the backend and Streamlit for the frontend. It leverages LangChain and Google Generative AI to provide intelligent responses.

## Features
- Real-time chatbot interaction
- Streamed responses from Google Generative AI
- Modern and user-friendly UI built with Streamlit

---

## Prerequisites
1. **Python**: Ensure Python 3.8 or later is installed.
2. **Dependencies**: Install required Python packages.
3. **Google API Key**: Obtain a valid Google API key for Generative AI.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/VirtualAdvisor.git
cd VirtualAdvisor
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
#### On Windows:
```bash
venv\Scripts\activate
```
#### On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

### 1. Start the Flask Backend
Navigate to the `backend` folder and run the Flask app:
```bash
cd backend
python app.py
```
The backend will start on `http://localhost:5001`.

### 2. Start the Streamlit Frontend
In a new terminal, navigate to the `backend` folder and run the Streamlit app:
```bash
streamlit run streamlit_ui.py
```
The frontend will start on `http://localhost:8501`.

---

## Environment Variables
Set the Google API key as an environment variable in a `.env` file:

### Use a `.env` File
1. Create a `.env` file in the `backend` directory.
2. Add the following line to the `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

---

## Usage
1. Open the Streamlit UI at `http://localhost:8501`.
2. Type your message in the input box and interact with the chatbot.

---

## Troubleshooting
- **Missing Dependencies**: Ensure all required packages are installed using `pip install -r requirements.txt`.
- **API Key Issues**: Verify your Google API key is valid and set correctly.
- **Port Conflicts**: Ensure ports `5001` (backend) and `8501` (frontend) are not in use by other applications.

---

## License
This project is licensed under the MIT License.
