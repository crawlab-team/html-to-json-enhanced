#!/usr/bin/env python
"""Convert html to json."""
from typing import List, Iterator, Union

import bs4


class HtmlConverter(object):
    def __init__(
        self,
        html_section,
        debug: bool,
        capture_element_values: bool,
        capture_element_attributes: bool,
        with_id: bool,
    ):
        self.html_section = html_section
        self.debug = debug
        self.capture_element_texts = capture_element_values
        self.capture_element_attributes = capture_element_attributes
        self.with_id = with_id

        self._element_id = 0

    @staticmethod
    def log_debug(debug, message, prefix=''):
        """Print the given message if debugging is true."""
        if debug:
            print('{}{}'.format(prefix, message))
            # add a newline after every message
            print('')

    def _debug(self, message, prefix=''):
        self.log_debug(self.debug, message, prefix)

    def _get_element_id(self):
        element_id = self._element_id
        self._element_id += 1
        return element_id

    @staticmethod
    def _record_element_texts(element, json_output):
        """Record the html element's value in the json_output."""
        text = element.strip()
        if text != '\n' and text != '':
            if json_output.get('_text'):
                json_output['_texts'] = [json_output['_text']]
                json_output['_texts'].append(text)
                del json_output['_text']
            elif json_output.get('_texts'):
                json_output['_texts'].append(text)
            else:
                json_output['_text'] = text

    def iterate(
        self,
        part: Union[bs4.element.Tag, bs4.element.NavigableString],
        json_output: dict,
        count: int,
        parent_id: int = None,
    ):
        """
        example json_output: {
            "_id": 1,
            "_parent": 0,
            "_tag": "div",
            "_attributes": {
                "id": "main",
                "class": ["container"]
            },
            "_children": [
                {...},
                {...},
                ...
            ],
            "_text": "some text",
        }
        """
        self._debug('========== Start New Iteration ==========', '    ' * count)
        self._debug('HTML_PART:\n{}'.format(part))
        self._debug('JSON_OUTPUT:\n{}'.format(json_output))

        if isinstance(part, bs4.element.Tag):
            # construct the new json output object
            if json_output.get('_tag') is None:
                json_output['_tag'] = part.name

            # record the element's id
            if self.with_id and json_output.get('_id') is None:
                json_output['_id'] = self._get_element_id()

            # record the element's parent id
            if self.with_id and parent_id is not None and json_output.get('_parent') is None:
                json_output['_parent'] = parent_id

            # record the element's attributes
            if self.capture_element_attributes and json_output.get('_attributes') is None:
                json_output['_attributes'] = part.attrs

            # record the element's children and texts
            if part.children is not None and json_output.get('_children') is None:
                for child in part.children:
                    if isinstance(child, bs4.element.Tag):
                        if json_output.get('_children') is None:
                            json_output['_children'] = []
                        json_output['_children'].append(
                            self.iterate(
                                child,
                                {},
                                count,
                                json_output['_id'],
                            )
                        )
                    elif isinstance(child, bs4.element.NavigableString):
                        self._record_element_texts(child, json_output)

        else:
            if self.capture_element_texts:
                self._record_element_texts(part, json_output)

        return json_output

    def convert(self):
        """Convert the html string to json."""
        soup = bs4.BeautifulSoup(self.html_section, 'html.parser')

        tags = [child for child in soup.contents if isinstance(child, bs4.element.Tag)]
        if len(tags) == 0:
            raise ValueError('No tags found in html section')
        else:
            root = tags[0]

        json_output = self.iterate(
            root,
            {},
            0,
        )

        return json_output


def _debug(debug, message, prefix=''):
    HtmlConverter.log_debug(debug, message, prefix)


def convert(
    html_string: str,
    debug: bool = False,
    capture_element_texts: bool = True,
    capture_element_attributes: bool = True,
    with_id: bool = True,
):
    return HtmlConverter(
        html_string,
        debug,
        capture_element_texts,
        capture_element_attributes,
        with_id,
    ).convert()


def iterate(json_output: dict, visited: set = None) -> Iterator[dict]:
    if visited is None:
        visited = set()

    if json_output.get('_id') is not None:
        if json_output['_id'] in visited:
            return

        visited.add(json_output['_id'])
        yield json_output

    if json_output.get('_children') is None:
        return

    for child in json_output.get('_children'):
        yield from iterate(child, visited)
