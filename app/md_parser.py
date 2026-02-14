import markdown
import frontmatter
from pygments.formatters import HtmlFormatter

def parse_markdown_file(file_path):
    """
    Parses a markdown file and returns a tuple of (metadata, html_content).
    Includes support for code highlighting and tables.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        
    # Extensions: 
    # 'fenced_code' for ```python blocks
    # 'codehilite' for syntax highlighting
    # 'tables' for data science data representation
    html_content = markdown.markdown(
        post.content, 
        extensions=['fenced_code', 'codehilite', 'tables', 'attr_list']
    )
    
    return post.metadata, html_content

def get_pygments_css():
    """Returns the CSS for syntax highlighting in code blocks."""
    return HtmlFormatter(style='monokai').get_style_defs('.codehilite')