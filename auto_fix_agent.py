import os
import sys
from langchain.llms import OpenAI
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

# Prepare prompt for LLM
prompt = PromptTemplate(
    input_variables=["log"],
    template="""
You are an expert Angular developer. The following test log contains failed tests. Analyze the log and suggest a code fix for the failure. Only output the code change needed, and explain briefly why it fixes the issue.

Test Log:
{log}
"""
)

llm = OpenAI(temperature=0)

response = llm(prompt.format(log=log_content))
print("\n--- Suggested Fix by Agentic Auto-Fix Layer ---\n")
print(response) 