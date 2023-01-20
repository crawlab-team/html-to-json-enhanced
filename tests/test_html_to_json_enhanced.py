import os.path
import unittest

from html_to_json_enhanced import convert, iterate


class TestHtmlToJsonWithId(unittest.TestCase):
    def setUp(self):
        self.html_strings = [
            {'html': """
<div class="col-md-4 tags-box">
    <h2>Top Ten tags</h2>
    <span class="tag-item">
        <a class="tag" style="font-size: 28px" href="/tag/love/">love</a>
    </span>
    <span class="tag-item">
        <a class="tag" style="font-size: 26px" href="/tag/inspirational/">inspirational</a>
    </span>
</div>
        """, 'max_id': 5},
            {'html': """
<div>
    <div>
        <div></div>
        <div>
            <div></div>
        </div>
    </div>
</div>
        """, 'max_id': 4},
        ]

        with open(os.path.join(os.path.dirname(__file__), 'data', 'http___quotes_toscrape_com_.html'), 'r') as f:
            self.html_strings.append({'html': f.read(), 'max_id': 150})

    def test_convert(self):
        output_json = convert(self.html_strings[0].get('html'))
        print(output_json)
        self.assertTrue(isinstance(output_json, dict))
        self.assertTrue(isinstance(output_json.get('_children'), list))
        self.assertTrue(isinstance(output_json.get('_children')[0], dict))
        for key in ['_tag', '_parent', '_id', '_attributes']:
            self.assertTrue(key in output_json.get('_children')[0].keys())
        self.assertTrue(isinstance(output_json.get('_children')[0].get('_id'), int))
        self.assertTrue(isinstance(output_json.get('_children')[0].get('_parent'), int))
        self.assertTrue(isinstance(output_json.get('_children')[0].get('_tag'), str))
        self.assertTrue(isinstance(output_json.get('_children')[0].get('_attributes'), dict))

    def test_iterate(self):
        for html_string in self.html_strings:
            is_dict = isinstance(html_string, dict)
            if is_dict:
                output_json = convert(html_string.get('html'), debug=False, with_id=True)
            else:
                output_json = convert(html_string, debug=False, with_id=True)

            ids = []
            for item in iterate(output_json):
                self.assertTrue(isinstance(item, dict))
                self.assertTrue(isinstance(item.get('_id'), int))
                self.assertTrue(isinstance(item.get('_tag'), str))
                if item.get('_parent') is not None:
                    self.assertTrue(isinstance(item.get('_parent'), int))
                ids.append(item.get('_id'))
            ids = sorted(ids)
            self.assertTrue(ids == list(range(len(ids))))

            if is_dict:
                self.assertEqual(html_string.get('max_id'), max(ids))


if __name__ == '__main__':
    unittest.main()
