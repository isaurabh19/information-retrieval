from bs4 import BeautifulSoup as bs
import json
import utils
import re

IGNORE_TAG = set(["table", "tr", "th", "tbody", "td", "img"])
NAV = "hatnote navigation-not-searchable"

class Parser(object):
    """Given a wikipedia document, parse and return the cleaned corpus
    """
    def __init__(self, page_source, case_fold=0, punctuation=1):
        self.page_source = page_source
        self.case_fold = case_fold
        self.punc = punctuation

    def remove_footer_content(self, page_source):
        """Removes `See Also', `Notes', `External Links', `References' sections
        from the page source 

        Return: String
        """        
        
        SEE_ALSO = "<span class=\"mw-headline\" id=\"See_also\">See also</span>"
        NOTES = "<span class=\"mw-headline\" id=\"Notes\">Notes</span>"
        EXTERNAL_LINKS = "<span class=\"mw-headline\" id=\"External_links\">External links</span>"
        REFERENCES = "<span class=\"mw-headline\" id=\"References\">References</span>"

        page_source_without_footer = None

        if SEE_ALSO in page_source:
            page_source_without_footer, _ = page_source.split(SEE_ALSO)
        elif NOTES in page_source:
            page_source_without_footer, _ = page_source.split(NOTES)
        elif REFERENCES in page_source:
            page_source_without_footer, _ = page_source.split(REFERENCES)
        elif EXTERNAL_LINKS in page_source:
            page_source_without_footer, _ = page_source.split(EXTERNAL_LINKS)
        else:
            page_source_without_footer = page_source

        return page_source_without_footer

    def filter_page_source(self):
        page_source_without_footer = self.remove_footer_content(self.page_source)
        if page_source_without_footer:
            soup = bs(page_source_without_footer, "html.parser")
            data = soup.find_all('div', attrs={"id":"mw-content-text"})
            child_tags = data[0].descendants
            body = ''
            
            for each_tag in child_tags:
                try:
                    if each_tag is not None and each_tag.name not in IGNORE_TAG and each_tag.get('id') != NAV:
                        body += each_tag.get_text()
                except AttributeError:
                    pass

            body = str(body.encode('utf-8'))

            # Option for Case Folding
            if self.case_fold == 1:
                body = body.lower()

            final_body_content = body
            # Option for Puntuation Handler
            if self.punc == 1:
                phandler = PunctuationHandler(body)
                final_body_content = phandler.clean()

            title = self.clean_title(soup.find('h1', attrs={"id": "firstHeading"}).text)
            packet = {
                "title": title,
                "content": final_body_content
            }
            return packet

    def clean_title(self, text):
        text = re.sub(r"\\x[0-9a-zA-Z]+[.,\s]*", "", text)
        text = re.sub(r"([\\]+')", "", text)
        text = re.sub(r"[\\]+", "", text)
        text.replace("/", "_")
        return text

class PunctuationHandler(object):
    """Given some text, remove necessary punctuations and return cleaned text
    """
    def __init__(self, text):
        self.text = text
        
    def clean(self):
        """Remove punctuation except hyphenated words.
        * removes unicode chars [\\x ...]
        * removes encoded carriage returns [\\n]
        * removes citattions [0-9]
        * remove encoded apostrophes [\\']
        * keeps numbers with commas [100,000,000]

        Returns: String
        """
        
        text = self.text

        # remove [edit]
        text = text.replace("[edit]", " ")

        # remove carriage returns
        text = re.sub(r"([\\]+n)+", " ", text)

        # numerics with comma
        currency = re.compile(r"(\d{1,3}(\,\d{3})*|(\d+))(\.\d{2})?")

        # remove utf-8 apostrophe; do this before removing puntuations
        text = re.sub(r"([\\]+')", "", text)

        # remove misc punctuations
        text = re.sub("[,\"^(){};/<>*!@#$%.+=|?`~:]+", lambda x: str(x) if currency.match(str(x)) else "", text)
        
        # remove citations
        text = re.sub(r"\[[0-9]+\]", " ", text)

        # remove unicode chars
        # updated \\x[0-9a-zA-Z]{2}
        text = re.sub(r"\\x[0-9a-zA-Z]+[.,\s]*", "", text)

        # finally remove extra \\
        text = re.sub(r"[\\]+", "", text)

        return text