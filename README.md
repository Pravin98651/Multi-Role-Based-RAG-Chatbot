# DS RPC 01: Internal chatbot with role based access control
Basic Authentication using FastAPI's `HTTPBasic` has been implemented in `main.py` for learners to get started with.


### Roles Provided
 - **engineering**
 - **finance**
 - **general**
 - **hr**
 - **marketing**


FinSolve Technologies, is a leading FinTech company providing innovative financial solutions and services to individuals, businesses, and enterprises.

Recently, teams have been facing delays in communication and difficulty accessing the right data at the right time, which has led to inefficiencies. These delays and data silos between different departments like Finance, Marketing, HR, and C-Level Executives have created roadblocks in decision-making, strategic planning, and project execution.

To address these challenges, Tony Sharma, the company’s Chief Innovation Officer, has launched a new project focusing on digital transformation through AI. He has reached out to Peter Pandey, an AI Engineer, who is ready to apply his recent learnings.

Tony proposed developing a role-based access control (RBAC) chatbot to reduce communication delays, address data access barriers, and offer secure, department-specific insights on demand. The aim is to design a chatbot that enables different teams to access role-specific data while maintaining secure access for Finance, Marketing, HR, C-Level Executives, and Employees.

Task:
Imagine yourself as Peter Pandey and develop a RAG-based role-based access control system for the chatbot, ensuring each user receives the correct data based on their role. The chatbot should process queries, retrieve data, and generate context-rich responses.

Roles and Permissions:

Finance Team: Access to financial reports, marketing expenses, equipment costs, reimbursements, etc.
Marketing Team: Access to campaign performance data, customer feedback, and sales metrics.
HR Team: Access employee data, attendance records, payroll, and performance reviews.
Engineering Department: Access to technical architecture, development processes, and operational guidelines.
C-Level Executives: Full access to all company data.
Employee Level: Access only to general company information such as policies, events, and FAQs.

Key Requirements:

Authentication and Role Assignment: The chatbot should authenticate users and assign them their roles.
Data Handling: Respond to queries based on the corresponding department data (Finance, Marketing, HR, General), also providing reference to the source document.
NLP: Process and understand natural language queries.
Role-Based Access Control: Ensure role-based data access.
 RAG: Retrieve data, augment it with context, and generate a clear, insightful response.

Tech Stack:

Python: Core programming language
FastAPI: Backend framework for the server
Use ChatGroq Llama or any LLM: Response generation
Vector Store (Qdrant, Chroma, Pinecone or any other): Document search and retrieval
Streamlit: Chatbot UI
Note: You're free to use any additional tools or technologies that enhance your solution.

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