import os
import sys
import subprocess
import re
import difflib
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

# Read the current file content
current_file_path = "src/app/dashboard/dashboard.component.spec.ts"
with open(current_file_path, "r") as f:
    current_content = f.readlines()

# Prepare the new content as lines
suggested_content = file_content.splitlines(keepends=True)

# Generate a unified diff
unified_diff = difflib.unified_diff(
    current_content,
    suggested_content,
    fromfile=current_file_path,
    tofile=current_file_path + ".suggested",
    lineterm=""
)

diff_output = "".join(line + "\n" for line in unified_diff)

diff_file_path = "src/app/dashboard/dashboard.component.spec.diff"
with open(diff_file_path, "w") as f:
    f.write(diff_output)

print(f"\n💡 Diff suggestion saved to {diff_file_path}. You can review and apply it manually.")
# (No file overwrite in CI mode) 