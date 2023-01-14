import os.path
import unittest

from html_to_json import convert, iterate


class TestHtmlToJsonWithId(unittest.TestCase):
    def setUp(self):
        self.html_strings = ["""<div class="col-md-4 tags-box">

                <h2>Top Ten tags</h2>

                <span class="tag-item">
                <a class="tag" style="font-size: 28px" href="/tag/love/">love</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 26px" href="/tag/inspirational/">inspirational</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 26px" href="/tag/life/">life</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 24px" href="/tag/humor/">humor</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 22px" href="/tag/books/">books</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 14px" href="/tag/reading/">reading</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 10px" href="/tag/friendship/">friendship</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 8px" href="/tag/friends/">friends</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 8px" href="/tag/truth/">truth</a>
                </span>

                <span class="tag-item">
                <a class="tag" style="font-size: 6px" href="/tag/simile/">simile</a>
                </span>


        </div>"""]

        with open(os.path.join(os.path.dirname(__file__), 'data', 'http___quotes_toscrape_com_.html'), 'r') as f:
            self.html_strings.append(f.read())

    def test_convert(self):
        output_json = convert(self.html_strings[0], debug=False, with_id=True)
        # print(output_json)
        self.assertTrue(isinstance(output_json, dict))
        self.assertTrue(isinstance(output_json.get('div'), list))
        for key in ['_attributes', '_id', '_tag']:
            self.assertTrue(key in output_json.get('div')[0])

    def test_iterate(self):
        for html_string in self.html_strings:
            output_json = convert(html_string, debug=False, with_id=True)

            ids = []
            for item in iterate(output_json):
                self.assertTrue(isinstance(item, dict))
                self.assertTrue(isinstance(item.get('_id'), int))
                self.assertTrue(isinstance(item.get('_tag'), str))
                ids.append(item.get('_id'))
            assert len(ids) > 0
            ids = sorted(ids)
            self.assertTrue(ids == list(range(len(ids))))


if __name__ == '__main__':
    unittest.main()
