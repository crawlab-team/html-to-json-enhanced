import unittest

from bs4 import BeautifulSoup

from html_to_json_enhanced.utils import get_css_path


class TestUtilsCssPath(unittest.TestCase):
    html_strings = [
        """
        <div class="col-md-4 tags-box">
            <h2>Top Ten tags</h2>
            <span class="tag-item">
                <a class="tag" style="font-size: 28px" href="/tag/love/">love</a>
            </span>
            <span class="tag-item">
                <a class="tag" style="font-size: 26px" href="/tag/inspirational/">inspirational</a>
            </span>
        </div>
        """
    ]

    def test_get_css_path(self):
        soup = BeautifulSoup(self.html_strings[0], 'html.parser')
        res = get_css_path(soup.select_one('.tag-item:nth-child(2)'))
        print(res)


if __name__ == '__main__':
    unittest.main()
