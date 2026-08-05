import os
import re

directory = r'\\wsl.localhost\Ubuntu\home\practicalace\projects\htmlcss'

# The old summary has 16 spaces for <summary>, 20 spaces for <h2>
old_summary_pattern = re.compile(
    r'( +)<summary>\s*<h2 style="display: inline; margin: 0;">📑 In This Lesson</h2>\s*</summary>',
    re.MULTILINE
)

# Using \1 for the 16 spaces, then 20 spaces for the spans
new_summary_template = r'''\1<summary aria-label="Toggle table of contents">
\1    <span class="toc-icon" aria-hidden="true">📑</span>
\1    <span class="toc-label">In This Lesson</span>
\1    <span class="toc-chevron" aria-hidden="true">▼</span>
\1</summary>'''

for filename in os.listdir(directory):
    if filename.startswith('lesson_') and filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use re.sub with a callback to ensure indentation is correct for each file if it varies
        def repl(match):
            indent = match.group(1)
            # 20 spaces for content inside summary (16 spaces + 4 spaces)
            inner_indent = indent + '    '
            return f'''{indent}<summary aria-label="Toggle table of contents">
{inner_indent}<span class="toc-icon" aria-hidden="true">📑</span>
{inner_indent}<span class="toc-label">In This Lesson</span>
{inner_indent}<span class="toc-chevron" aria-hidden="true">▼</span>
{indent}</summary>'''

        if old_summary_pattern.search(content):
            new_content = old_summary_pattern.sub(repl, content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {filename}')
        else:
            print(f'Skipped {filename} (summary pattern not found)')
