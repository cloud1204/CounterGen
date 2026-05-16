import re
import os
from bs4 import BeautifulSoup, NavigableString, Tag

def codeforces_html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Locate the root wrapper of the problem statement
    prob_stmt = soup.find('div', class_='problem-statement')
    if not prob_stmt:
        return "Error: Could not find the 'problem-statement' class element in the HTML file."

    markdown_parts = []

    # Recursive helper to handle Codeforces inline formatting and structural elements
    def process_node(node):
        if isinstance(node, NavigableString):
            return str(node)
        
        if isinstance(node, Tag):
            # Italicized terms
            if node.name == 'span' and 'tex-font-style-it' in node.get('class', []):
                return f" *{process_children(node).strip()}* "
            # Monospaced values / code fonts
            elif node.name == 'span' and 'tex-font-style-tt' in node.get('class', []):
                return f" `{process_children(node).strip()}` "
            # Paragraphs
            elif node.name == 'p':
                return f"{process_children(node)}\n\n"
            # Lists
            elif node.name == 'ul':
                return f"\n{process_children(node)}"
            elif node.name == 'li':
                return f"- {process_children(node).strip()}\n"
            # Footnotes at the bottom of sections
            elif node.name == 'div' and 'statement-footnote' in node.get('class', []):
                return f"\n---\n\n*{process_children(node).strip()}*\n"
            else:
                return process_children(node)
        return ""

    def process_children(tag):
        return "".join(process_node(child) for child in tag.children)

    def clean_text_and_math(text):
        # Codeforces uses $$$ for math blocks. Standard markdown engines use $ (inline) or $$ (block).
        # Replacing $$$ with $ correctly handles both inline and converts $$$ $$$ blocks to $$ blocks.
        text = text.replace('$$$', '$')
        # Clean up excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    # 1. Parse Header Info (Title, Limits)
    header = prob_stmt.find('div', class_='header')
    if header:
        title = header.find('div', class_='title')
        time_lim = header.find('div', class_='time-limit')
        mem_lim = header.find('div', class_='memory-limit')
        
        if title:
            markdown_parts.append(f"# {title.get_text().strip()}\n")
        if time_lim:
            markdown_parts.append(f"**Time Limit:** {time_lim.get_text().replace('time limit per test', '').strip()}")
        if mem_lim:
            markdown_parts.append(f"**Memory Limit:** {mem_lim.get_text().replace('memory limit per test', '').strip()}\n")
        markdown_parts.append("---\n")

    # 2. Parse Main Problem Description
    desc_nodes = []
    for child in prob_stmt.children:
        if isinstance(child, Tag):
            # Skip metadata headers, specs, samples and notes
            if child.get('class') and any(cls in child.get('class') for cls in ['header', 'input-specification', 'output-specification', 'sample-tests', 'note']):
                continue
            desc_nodes.append(process_node(child))
    
    if desc_nodes:
        markdown_parts.append("## Problem Statement\n")
        markdown_parts.append("".join(desc_nodes).strip() + "\n")

    # 3. Parse Input Specification
    input_spec = prob_stmt.find('div', class_='input-specification')
    if input_spec:
        markdown_parts.append("\n## Input Specification\n")
        content = ''.join(process_node(child) for child in input_spec.children if not (isinstance(child, Tag) and 'section-title' in child.get('class', [])))
        markdown_parts.append(content.strip() + "\n")

    # 4. Parse Output Specification
    output_spec = prob_stmt.find('div', class_='output-specification')
    if output_spec:
        markdown_parts.append("\n## Output Specification\n")
        content = ''.join(process_node(child) for child in output_spec.children if not (isinstance(child, Tag) and 'section-title' in child.get('class', [])))
        markdown_parts.append(content.strip() + "\n")

    # 5. Parse Example Test Cases
    sample_tests = prob_stmt.find('div', class_='sample-tests')
    if sample_tests:
        markdown_parts.append("\n## Examples\n")
        samples = sample_tests.find_all('div', class_='sample-test')
        for sample in samples:
            inputs = sample.find_all('div', class_='input')
            outputs = sample.find_all('div', class_='output')
            
            for index, (inp, outp) in enumerate(zip(inputs, outputs), start=1):
                in_pre = inp.find('pre')
                out_pre = outp.find('pre')
                
                # Codeforces wraps each test line inside a div class='test-example-line'
                in_text = ""
                if in_pre:
                    lines = in_pre.find_all('div', class_='test-example-line')
                    in_text = "\n".join(line.get_text() for line in lines) if lines else in_pre.get_text()
                        
                out_text = ""
                if out_pre:
                    lines = out_pre.find_all('div', class_='test-example-line')
                    out_text = "\n".join(line.get_text() for line in lines) if lines else out_pre.get_text()
                
                markdown_parts.append(f"### Example {index}\n")
                markdown_parts.append("**Input:**\n```\n" + in_text.strip() + "\n```\n")
                markdown_parts.append("**Output:**\n```\n" + out_text.strip() + "\n```\n")

    # 6. Parse Explanation Note Section
    note_sec = prob_stmt.find('div', class_='note')
    if note_sec:
        markdown_parts.append("\n## Note\n")
        content = ''.join(process_node(child) for child in note_sec.children if not (isinstance(child, Tag) and 'section-title' in child.get('class', [])))
        markdown_parts.append(content.strip() + "\n")

    # Synthesize everything and clean syntax
    full_markdown = "\n".join(markdown_parts)
    return clean_text_and_math(full_markdown)


if __name__ == "__main__":
    input_filename = "statement.txt"
    output_filename = "statement.md"

    # Check if the file exists before running
    if not os.path.exists(input_filename):
        print(f"Error: '{input_filename}' not found in the current directory.")
        print("Please save the raw HTML source of the Codeforces page into 'statement.txt' first.")
    else:
        # Read the local HTML document
        with open(input_filename, "r", encoding="utf-8") as f:
            html_data = f.read()
        
        print(f"Parsing '{input_filename}'...")
        markdown_output = codeforces_html_to_markdown(html_data)
        
        # Write the output to a .md file
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(markdown_output)
            
        print(f"Success! Saved formatted problem statement to '{output_filename}'")