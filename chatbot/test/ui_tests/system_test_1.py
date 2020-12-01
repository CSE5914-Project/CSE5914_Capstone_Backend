from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("http://localhost:3000/")

        ## login
        self.click('button[class="ant-btn ant-btn-primary ant-btn-round"]')
        self.type('input[placeholder="user123"]', "asdfdsagdsagdsafsd")
        self.click('button[class="ant-btn ant-btn-primary"]')
        self.click('button[class="ant-btn ant-btn-primary"]')

        ## chatbot
        self.type('input[placeholder="Write your message here"]', "action")
        self.click('button[class="react-chatbot-kit-chat-btn-send"]')
        
        ## movie show up
        self.assert_element("div[class='ant-card-cover']")

        # self.assert_text("xkcd: volume 0", "h3")
        # self.open("https://xkcd.com/353/")
        # self.assert_title("xkcd: Python")
        # self.assert_element('img[alt="Python"]')
        # self.click('a[rel="license"]')
        # self.assert_text("free to copy and reuse")
        # self.go_back()
        # self.click_link_text("About")
        # self.assert_exact_text("xkcd.com", "h2")
        # self.click_link_text("geohashing")
        # self.assert_element("#comic img")
        
