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

(Note: This is the specs of my system so we are going to use the following specs 
ASUS VivoBook 15 AMD Ryzen 7 Octa Core 5800HS - (16 GB/512 GB SSD/Windows 11 Home) M1502QA-EJ742WS Thin and Light Laptop  (15.6 Inch, Cool Silver, 1.70 kg, With MS Office)
)