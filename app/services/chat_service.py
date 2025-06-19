import os
from typing import List, Dict
from groq import Groq
from .document_processor import DocumentProcessor
import tiktoken
import re
import pandas as pd
from io import StringIO

class ChatService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.document_processor = DocumentProcessor()
        self.model = "Qwen-qwq-32b"
        self.max_tokens = 3500  # Strict context limit for Groq API
        self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Closest available for Groq models
        self.hr_df = self.load_hr_csv()

    def load_hr_csv(self):
        # Find and load the full hr_data.csv as a DataFrame
        hr_path = None
        for role_dir in self.document_processor.data_dir.iterdir():
            if role_dir.is_dir() and role_dir.name == 'hr':
                for file_path in role_dir.glob("*.csv"):
                    if file_path.name == 'hr_data.csv':
                        hr_path = file_path
                        break
        if hr_path:
            try:
                return pd.read_csv(hr_path)
            except Exception as e:
                print(f"Error loading hr_data.csv: {e}")
        return None

    def estimate_tokens(self, text: str) -> int:
        # Use tiktoken for accurate token counting
        return len(self.tokenizer.encode(text))

    def extract_employee_details(self, query: str, context: List[Dict]) -> str:
        # Look for an employee ID in the query
        match = re.search(r'FINEMP\d{4}', query)
        if not match:
            return None
        emp_id = match.group(0)
        # Search for the employee in CSV chunks
        for doc in context:
            if doc['metadata']['source'].endswith('.csv'):
                # Try to parse the chunk as a CSV
                try:
                    # Only parse if the chunk contains the employee ID
                    if emp_id in doc['document']:
                        # Try to parse the chunk as a CSV table
                        csv_text = doc['document']
                        # Add header if missing (first chunk has header)
                        if 'employee_id' not in csv_text.split('\n')[0]:
                            csv_text = 'employee_id,full_name,role,department,email,location,date_of_birth,date_of_joining,manager_id,salary,leave_balance,leaves_taken,attendance_pct,performance_rating,last_review_date\n' + csv_text
                        df = pd.read_csv(StringIO(csv_text))
                        row = df[df['employee_id'] == emp_id]
                        if not row.empty:
                            info = row.iloc[0]
                            return f"Employee ID: {info['employee_id']}\nFull Name: {info['full_name']}\nRole: {info['role']}\nDepartment: {info['department']}\nEmail: {info['email']}\nLocation: {info['location']}\nDate of Birth: {info['date_of_birth']}\nDate of Joining: {info['date_of_joining']}\nManager ID: {info['manager_id']}\nSalary: {info['salary']}\nLeave Balance: {info['leave_balance']}\nLeaves Taken: {info['leaves_taken']}\nAttendance %: {info['attendance_pct']}\nPerformance Rating: {info['performance_rating']}\nLast Review Date: {info['last_review_date']}"
                except Exception as e:
                    continue
        return None

    def extract_hr_table_query(self, query: str, context: List[Dict]) -> str:
        # Aggregate all CSV chunks
        dfs = []
        for doc in context:
            if doc['metadata']['source'].endswith('.csv'):
                try:
                    csv_text = doc['document']
                    if 'employee_id' not in csv_text.split('\n')[0]:
                        csv_text = 'employee_id,full_name,role,department,email,location,date_of_birth,date_of_joining,manager_id,salary,leave_balance,leaves_taken,attendance_pct,performance_rating,last_review_date\n' + csv_text
                    df = pd.read_csv(StringIO(csv_text))
                    dfs.append(df)
                except Exception as e:
                    continue
        if not dfs:
            return None
        df_all = pd.concat(dfs, ignore_index=True)
        # List all employee IDs
        if re.search(r'(all )?employee id(s)?', query, re.I):
            ids = df_all['employee_id'].drop_duplicates().tolist()
            return 'Employee IDs:\n' + '\n'.join(ids)
        # List all roles
        if re.search(r'(all )?role(s)?( available)?', query, re.I):
            roles = df_all['role'].drop_duplicates().tolist()
            return 'Roles:\n' + '\n'.join(roles)
        # List all employees with a specific role/title
        match = re.search(r'(?:employees? who (?:are|is)|employees? with|name (?:the )?employees? (?:who )?(?:are|is|with)?|list (?:the )?employees? (?:who )?(?:are|is|with)?) ([\w\s]+)', query, re.I)
        if match:
            role_query = match.group(1).strip().lower()
            # Try to match role exactly or partially
            mask = df_all['role'].str.lower().str.contains(role_query)
            names = df_all.loc[mask, 'full_name'].drop_duplicates().tolist()
            if names:
                return f"Employees with role '{role_query}':\n" + '\n'.join(names)
            else:
                return f"No employees found with role '{role_query}'."
        return None

    def answer_hr_query(self, query: str) -> str:
        if self.hr_df is None:
            return None
        df = self.hr_df
        q = query.lower()
        # List all employee IDs
        if re.search(r'(all )?employee id(s)?', q):
            ids = df['employee_id'].drop_duplicates().tolist()
            return 'Employee IDs:\n' + '\n'.join(ids)
        # List all roles
        if re.search(r'(all )?role(s)?( available)?', q):
            roles = df['role'].drop_duplicates().tolist()
            return 'Roles:\n' + '\n'.join(roles)
        # List all departments
        if re.search(r'(all )?department(s)?', q):
            depts = df['department'].drop_duplicates().tolist()
            return 'Departments:\n' + '\n'.join(depts)
        # List all employees with a specific role/title
        match = re.search(r'(?:employees? who (?:are|is)|employees? with|name (?:the )?employees? (?:who )?(?:are|is|with)?|list (?:the )?employees? (?:who )?(?:are|is|with)?) ([\w\s]+)', q)
        if match:
            role_query = match.group(1).strip().lower()
            mask = df['role'].str.lower().str.contains(role_query)
            names = df.loc[mask, 'full_name'].drop_duplicates().tolist()
            if names:
                return f"Employees with role '{role_query}':\n" + '\n'.join(names)
            else:
                return f"No employees found with role '{role_query}'."
        # List all employees in a department
        match = re.search(r'(?:employees? in|list employees? in|show employees? in|who works in) ([\w\s]+)', q)
        if match:
            dept_query = match.group(1).strip().lower()
            mask = df['department'].str.lower().str.contains(dept_query)
            names = df.loc[mask, 'full_name'].drop_duplicates().tolist()
            if names:
                return f"Employees in department '{dept_query}':\n" + '\n'.join(names)
            else:
                return f"No employees found in department '{dept_query}'."
        # List all employees in a location
        match = re.search(r'(?:employees? in|list employees? in|show employees? in|who works in) ([\w\s]+)', q)
        if match:
            loc_query = match.group(1).strip().lower()
            mask = df['location'].str.lower().str.contains(loc_query)
            names = df.loc[mask, 'full_name'].drop_duplicates().tolist()
            if names:
                return f"Employees in location '{loc_query}':\n" + '\n'.join(names)
            else:
                return f"No employees found in location '{loc_query}'."
        # Find manager of an employee
        match = re.search(r'(?:manager of|who manages|who is the manager of) ([\w\s]+)', q)
        if match:
            emp_query = match.group(1).strip().lower()
            row = df[df['full_name'].str.lower().str.contains(emp_query)]
            if not row.empty:
                manager_id = row.iloc[0]['manager_id']
                manager_row = df[df['employee_id'] == manager_id]
                if not manager_row.empty:
                    manager_name = manager_row.iloc[0]['full_name']
                    return f"Manager of {row.iloc[0]['full_name']}: {manager_name} (ID: {manager_id})"
                else:
                    return f"Manager ID for {row.iloc[0]['full_name']}: {manager_id} (not found in data)"
            else:
                return f"No employee found with name '{emp_query}'."
        # Find all details for a given employee ID or name
        match = re.search(r'finemp\d{4}', q)
        if match:
            emp_id = match.group(0).upper()
            row = df[df['employee_id'] == emp_id]
            if not row.empty:
                info = row.iloc[0]
                return f"Employee ID: {info['employee_id']}\nFull Name: {info['full_name']}\nRole: {info['role']}\nDepartment: {info['department']}\nEmail: {info['email']}\nLocation: {info['location']}\nDate of Birth: {info['date_of_birth']}\nDate of Joining: {info['date_of_joining']}\nManager ID: {info['manager_id']}\nSalary: {info['salary']}\nLeave Balance: {info['leave_balance']}\nLeaves Taken: {info['leaves_taken']}\nAttendance %: {info['attendance_pct']}\nPerformance Rating: {info['performance_rating']}\nLast Review Date: {info['last_review_date']}"
        match = re.search(r'(?:details for|show details for|info for|information for|find) ([\w\s]+)', q)
        if match:
            emp_query = match.group(1).strip().lower()
            row = df[df['full_name'].str.lower().str.contains(emp_query)]
            if not row.empty:
                info = row.iloc[0]
                return f"Employee ID: {info['employee_id']}\nFull Name: {info['full_name']}\nRole: {info['role']}\nDepartment: {info['department']}\nEmail: {info['email']}\nLocation: {info['location']}\nDate of Birth: {info['date_of_birth']}\nDate of Joining: {info['date_of_joining']}\nManager ID: {info['manager_id']}\nSalary: {info['salary']}\nLeave Balance: {info['leave_balance']}\nLeaves Taken: {info['leaves_taken']}\nAttendance %: {info['attendance_pct']}\nPerformance Rating: {info['performance_rating']}\nLast Review Date: {info['last_review_date']}"
        # List all employees
        if re.search(r'(all )?employees?$', q) or re.search(r'list (all )?employees?', q):
            names = df['full_name'].drop_duplicates().tolist()
            return 'All Employees:\n' + '\n'.join(names)
        return None

    def generate_response(self, role: str, query: str, context: List[Dict] = None) -> str:
        """Generate a response using the LLM with context, limiting total tokens. Retrieve from all files/chunks."""
        if role == 'hr':
            hr_answer = self.answer_hr_query(query)
            if hr_answer:
                return hr_answer
        if context is None:
            # Retrieve fewer chunks to avoid overfilling the prompt
            context = self.document_processor.get_relevant_documents('all', query, n_results=10)

        context_str = ""
        total_tokens = 0
        for doc in context:
            doc_str = f"Source: {doc['metadata']['source']} (chunk {doc['metadata'].get('chunk_index', 0)})\nContent: {doc['document']}\n\n"
            doc_tokens = self.estimate_tokens(doc_str)
            if total_tokens + doc_tokens > self.max_tokens:
                break
            context_str += doc_str
            total_tokens += doc_tokens

        # Also count tokens for the prompt instructions and user query
        prompt = f"""You are an AI assistant for FinSolve Technologies. You have access to the following context:\n\n{context_str}\nUser Query: {query}\n\nPlease provide a helpful response based on the context above. If the context doesn't contain relevant information, please say so. Cite the source file(s) and chunk(s) you used."""
        # If prompt is still too large, truncate context_str further
        while self.estimate_tokens(prompt) > self.max_tokens and '\n\n' in context_str:
            # Remove the last chunk
            context_str = '\n\n'.join(context_str.strip().split('\n\n')[:-1]) + '\n\n'
            prompt = f"""You are an AI assistant for FinSolve Technologies. You have access to the following context:\n\n{context_str}\nUser Query: {query}\n\nPlease provide a helpful response based on the context above. If the context doesn't contain relevant information, please say so. Cite the source file(s) and chunk(s) you used."""

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for FinSolve Technologies."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        return completion.choices[0].message.content 