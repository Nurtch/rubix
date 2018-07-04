from IPython.display import HTML, display, Markdown


def print_html_table(data):
    '''
    Takes in a list of list as data and prints an HTML table
    '''
    display(HTML(
        '<table><tr>{}</tr></table>'.format(
            '</tr><tr>'.join(
                '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
            )
     ))


def print_markdown_table(headers, data):
    '''
    Renders table given headers and data
    '''
    md = ''

    for h in headers:
        md += '|' + h

    md += '|\n'

    for r in range(len(headers)):
        md += '|---'

    md += '|\n'

    for row in data:
        for element in row:
            md += '|' + str(element)
        md += '|\n'

    display(Markdown(md))


def first(iterable, default=None):
    '''
    Returns the first item from iterable. If no items then returns default
    '''
    for item in iterable:
      return item

    return default


def printmd(string):
    '''
    Renders markdown in notebook output of codecell
    '''
    display(Markdown(string))
