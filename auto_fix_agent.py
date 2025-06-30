import os
import sys
import subprocess
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Read test log file
log_file = sys.argv[1] if len(sys.argv) > 1 else 'test.log'
if not os.path.exists(log_file):
    print(f'Log file {log_file} not found.')
    sys.exit(1)

with open(log_file, 'r') as f:
    log_content = f.read()

# Check for failed tests
if 'FAILED' not in log_content and 'Error' not in log_content:
    print('No failed tests detected.')
    sys.exit(0)

# Prompt for full file content
prompt = PromptTemplate(
    input_variables=["log"],
    template="""
You are an expert Angular developer. The following test log contains failed tests.
Analyze the log and provide the full corrected content of src/app/dashboard/dashboard.component.spec.ts.
Respond with only the code in a single markdown block.

Test Log:
{log}
"""
)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

response = llm.invoke(prompt.format(log=log_content))
file_content_match = re.search(r"```[a-zA-Z]*\n([\s\S]*?)```", response.content)

if not file_content_match:
    print("Could not find a code block in the LLM response.")
    sys.exit(1)

file_content = file_content_match.group(1)

with open("src/app/dashboard/dashboard.component.spec.ts", "w") as f:
    f.write(file_content)

print("\n✅ File overwritten with agentic fix!") 