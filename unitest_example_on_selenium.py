import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

# The setUp is part of initialization, this method will get called before every test function which you are going to write in this test case class. Here you are creating the instance of Chrome WebDriver.
    def setUp(self):
        self.driver = webdriver.Chrome()

# This is the test case method. The test case method should always start with characters test. The first line inside this method create a local reference to the driver object created in setUp method.
    def test_search_in_python_org(self):
        # The driver.get method will navigate to a page given by the URL. WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired) before returning control to your test or script. Be aware that if your page uses a lot of AJAX on load then WebDriver may not know when it has completely loaded:
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)

        # WebDriver offers a number of ways to find elements using one of the find_element_by_* methods. For example, the input text element can be located by its name attribute using find_element_by_name method. Detailed explanation of finding elements is available in the Locating Elements chapter: https://selenium-python.readthedocs.io/locating-elements.html#locating-elements
        elem = driver.find_element_by_name("q")
        # Next, we are sending keys, this is similar to entering keys using your keyboard. Special keys can be send using Keys class imported from selenium.webdriver.common.keys:
        elem.send_keys("pycon")
        # After submission of the page, you should get the result as per search if there is any. To ensure that some results are found, make an assertion:
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        # Note: 1) 

    # The tearDown method will get called after every test method. This is a place to do all cleanup actions. In the current method, the browser window is closed. You can also call quit method instead of close. The quit will exit the entire browser, whereas close will close a tab, but if it is the only tab opened, by default most browser will exit entirely.:
    def tearDown(self):
        self.driver.close()


# Final lines are some boiler plate code to run the test suite:
if __name__ == "__main__":
    unittest.main()
# To run the above test in Ipython or Jupyter, you should pass a coupld of argument to the main function as shown below:
# unittest.main(argv=['first-arg-is-ignored'], exit=False)