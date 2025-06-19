# FinSolve Chatbot Setup Guide

## Prerequisites
- Python 3.10 or higher
- Groq API key (get one for free at https://console.groq.com/)

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Sample Data**
   The system comes with sample documents for each role:
   - `resources/data/engineering/architecture.txt` - System architecture
   - `resources/data/finance/reports.txt` - Financial reports
   - `resources/data/hr/policies.txt` - HR policies
   - `resources/data/marketing/campaigns.txt` - Marketing campaigns
   - `resources/data/general/company_info.txt` - Company information

4. **Start the Application**

   **Option A: Using the startup script**
   ```bash
   python run_app.py
   ```

   **Option B: Manual startup**
   
   Terminal 1 (FastAPI server):
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Terminal 2 (Streamlit UI):
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Usage

1. Open your browser and go to `http://localhost:8501`
2. Log in with one of the test credentials:
   - Username: `Tony`, Password: `password123` (Engineering)
   - Username: `Bruce`, Password: `securepass` (Marketing)
   - Username: `Sam`, Password: `financepass` (Finance)
   - Username: `Natasha`, Password: `hrpass123` (HR)

3. Start chatting! The chatbot will provide role-specific responses based on your access level.

## API Endpoints

- `GET /login` - Login endpoint
- `GET /test` - Test endpoint
- `POST /chat` - Chat endpoint (requires authentication)

## Project Structure

```
├── app/
│   ├── main.py              # FastAPI application
│   ├── streamlit_app.py     # Streamlit UI
│   └── services/
│       ├── vector_store.py      # FAISS vector store
│       ├── document_processor.py # Document processing
│       └── chat_service.py      # LLM integration
├── resources/
│   └── data/               # Role-specific documents
├── requirements.txt        # Python dependencies
└── run_app.py             # Startup script
```

## Technical Details

- **Vector Store**: FAISS (Facebook AI Similarity Search) for efficient similarity search
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: Groq API for response generation
- **Backend**: FastAPI with role-based authentication
- **Frontend**: Streamlit for the chat interface

## Troubleshooting

1. **Import Errors**: Make sure all dependencies are installed
2. **API Key Issues**: Verify your Groq API key is correct
3. **Port Conflicts**: Change ports in the startup commands if needed
4. **Document Loading**: Ensure documents are in the correct role directories
5. **Memory Issues**: FAISS indices are stored on disk and loaded as needed 