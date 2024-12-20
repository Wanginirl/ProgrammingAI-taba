import nbformat as nbf
import re

def create_notebook_from_py(py_file, ipynb_file):
    # Read the Python file
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create a new notebook
    nb = nbf.v4.new_notebook()
    cells = []

    # Split the content by cell markers
    cell_contents = re.split(r'# %%(?:\s*\[markdown\])?', content)

    for cell_content in cell_contents:
        if not cell_content.strip():
            continue
            
        # Determine if it's a markdown cell
        is_markdown = bool(re.match(r'^#.*', cell_content.strip()))
        
        if is_markdown:
            # Remove leading '#' and spaces from each line
            markdown_content = '\n'.join(
                line[1:].lstrip() if line.startswith('#') else line
                for line in cell_content.strip().split('\n')
            )
            cells.append(nbf.v4.new_markdown_cell(markdown_content))
        else:
            cells.append(nbf.v4.new_code_cell(cell_content.strip()))

    nb.cells = cells

    # Write the notebook to a file
    with open(ipynb_file, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

if __name__ == '__main__':
    py_file = 'economic_analysis_with_mongodb.py'
    ipynb_file = 'economic_analysis_with_mongodb.ipynb'
    create_notebook_from_py(py_file, ipynb_file)
    print(f"Successfully converted {py_file} to {ipynb_file}")
