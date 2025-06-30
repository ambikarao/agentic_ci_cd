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

# Prepare prompt for LLM
prompt = PromptTemplate(
    input_variables=["log"],
    template="""
You are an expert Angular developer and a git tool. The following test log contains failed tests.
Analyze the log and provide a fix as a git diff.
Your response must contain ONLY the git diff inside a single markdown code block.

Example response:
```diff
--- a/src/app/app.component.spec.ts
+++ b/src/app/app.component.spec.ts
@@ -25,7 +25,7 @@
   it('should render title', () => {
     const fixture = TestBed.createComponent(AppComponent);
     fixture.detectChanges();
     const compiled = fixture.nativeElement as HTMLElement;
-    expect(compiled.querySelector('h1')?.textContent).toContain('Hello, agentic_ci_cd_experiment');
+    expect(compiled.querySelector('h1')?.textContent).toContain('Hello, world');
   });
 });
```

Test Log:
{log}
"""
)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

response = llm.invoke(prompt.format(log=log_content))
fix_content = response.content

print("\n--- Suggested Fix by Agentic Auto-Fix Layer ---\n")
print(fix_content)

# Extract diff content
diff_match = re.search(r"```diff\n(.*?)```", fix_content, re.DOTALL)

if not diff_match:
    print("Could not find a diff in the LLM response.")
    sys.exit(1)

diff_content = diff_match.group(1)
with open("fix.patch", "w") as f:
    f.write(diff_content)

# Apply the patch
try:
    subprocess.run(["git", "apply", "fix.patch"], check=True)
    print("\n✅ Patch applied successfully!")
except subprocess.CalledProcessError as e:
    print(f"\n❌ Failed to apply patch: {e}")
    sys.exit(1) 