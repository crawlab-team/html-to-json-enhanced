from typing import Union, List


def _get_node_css_selector_repr(node, parent=None) -> str:
    tag: Union[str, None] = node.name if node.name != '[document]' else None
    classes: List[str] = node.attrs.get('class', [])
    path = []
    if tag is not None:
        path.append(tag)
    if len(classes) > 0:
        path.append('.' + '.'.join(classes))

    node_path = ''.join(path)


def _get_element(node):
    # for XPATH we have to count only for nodes with same type!
    length = len(list(node.previous_siblings)) + 1
    if length > 1:
        return '%s:nth-child(%s)' % (node.name, length)
    else:
        if node.name == '[document]':
            return '/'
        else:
            return node.name


def get_css_path(node):
    path = [_get_element(node)]
    for parent in node.parents:
        if parent.name == 'body':
            break
        path.insert(0, _get_element(parent))
    return ' > '.join(path)
