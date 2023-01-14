#!/usr/bin/env python
"""Convert html to json."""
from typing import List, Iterator, Union

import bs4


def _debug(debug, message, prefix=''):
    """Print the given message if debugging is true."""
    if debug:
        print('{}{}'.format(prefix, message))
        # add a newline after every message
        print('')


def _record_element_value(element, json_output, with_id: bool, element_id: int) -> int:
    """Record the html element's value in the json_output."""
    element = element.strip()
    if element != '\n' and element != '':
        if json_output.get('_value'):
            json_output['_values'] = [json_output['_value']]
            json_output['_values'].append(element)
            del json_output['_value']
        elif json_output.get('_values'):
            json_output['_values'].append(element)
        else:
            json_output['_value'] = element

        # record the element's id
        if with_id and json_output.get('_id') is None:
            json_output['_id'] = element_id
            element_id += 1

    return element_id


def _iterate(
    html_section,
    json_output: dict,
    count: int,
    debug: bool,
    capture_element_values: bool,
    capture_element_attributes: bool,
    with_id: bool,
    element_id: int = 0,
):
    _debug(debug, '========== Start New Iteration ==========', '    ' * count)
    _debug(debug, 'HTML_SECTION:\n{}'.format(html_section))
    _debug(debug, 'JSON_OUTPUT:\n{}'.format(json_output))

    for part in html_section:
        if not isinstance(part, str):
            # for python2 - check if part is unicode
            try:
                string_is_unicode = isinstance(part, unicode)
            # for python3 - catch error when trying to use the name 'unicode'
            except NameError:
                string_is_unicode = False
            # no matter what - keep going
            finally:
                # if part is not unicode, record it
                if not string_is_unicode:
                    # construct the new json output object
                    if not json_output.get(part.name):
                        json_output[part.name] = list()

                    # construct the new json child object
                    new_json_output_for_subparts = dict()

                    # record the element's attributes
                    if part.attrs and capture_element_attributes:
                        new_json_output_for_subparts = {'_attributes': part.attrs}

                    # record the element's id
                    if with_id:
                        new_json_output_for_subparts['_id'] = element_id
                        element_id += 1

                    # record the element's tag
                    # if part.name:
                    new_json_output_for_subparts['_tag'] = part.name

                    # increment the count
                    count += 1

                    # append to json output
                    json_output[part.name].append(
                        _iterate(
                            part,
                            new_json_output_for_subparts,
                            count,
                            debug=debug,
                            capture_element_values=capture_element_values,
                            capture_element_attributes=capture_element_attributes,
                            with_id=with_id,
                            element_id=element_id,
                        )
                    )
                # this will only be true in python2 - handle an entry that is unicode
                else:
                    if capture_element_values:
                        element_id = _record_element_value(part, json_output, with_id, element_id)
        else:
            if capture_element_values:
                element_id = _record_element_value(part, json_output, with_id, element_id)
    return json_output


def convert(
    html_string: str,
    debug: bool = False,
    capture_element_values: bool = True,
    capture_element_attributes: bool = True,
    with_id: bool = False,
):
    """Convert the html string to json."""
    soup = bs4.BeautifulSoup(html_string, 'html.parser')
    children = [child for child in soup.contents]
    return _iterate(
        children,
        {},
        0,
        debug=debug,
        capture_element_values=capture_element_values,
        capture_element_attributes=capture_element_attributes,
        with_id=with_id,
    )


def iterate(json_output: dict, visited: set = None) -> Iterator[dict]:
    if visited is None:
        visited = set()

    if json_output.get('_id') is not None:
        if json_output['_id'] in visited:
            return

        if json_output.get('_tag') is None:
            json_output['_tag'] = 'root'

        visited.add(json_output['_id'])
        yield json_output

    for key, children in json_output.items():
        if key.startswith('_'):
            continue

        for child in children:
            for grandchild in iterate(child, visited):
                yield grandchild