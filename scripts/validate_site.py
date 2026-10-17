"""Offline validation of the public static site; no remote service is required."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import re, unittest

ROOT = Path(__file__).resolve().parents[1]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[];self.ids=set();self.links=[];self.headings=[];self.scripts=[];self.attrs=[];self.errors=[];self.tags=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs);self.attrs.append((tag,attrs));self.tags.append(tag)
        if tag not in VOID:self.stack.append(tag)
        if "id" in attrs:
            if attrs["id"] in self.ids:self.errors.append("Duplicate id: "+attrs["id"])
            self.ids.add(attrs["id"])
        if "href" in attrs:self.links.append(attrs["href"])
        if tag in {"h1","h2","h3"}:self.headings.append(tag)
        if tag=="script":self.scripts.append(attrs)
        for name in attrs:
            if name.startswith("on"):self.errors.append("Inline event handler")
    def handle_endtag(self,tag):
        if not self.stack or self.stack[-1]!=tag:self.errors.append("Mismatched tag: "+tag)
        else:self.stack.pop()

def pages():
    result={}
    for path in ROOT.glob("*.html"):
        page=Page();page.feed(path.read_text(encoding="utf-8"));result[path.name]=page
    return result

class SiteTests(unittest.TestCase):
    def test_semantic_structure_and_language(self):
        for name,page in pages().items():
            self.assertEqual([],page.errors,name);self.assertEqual([],page.stack,name)
            self.assertEqual(1,page.headings.count("h1"),name)
            for tag in ["header","nav","main","footer","title"]:self.assertIn(tag,page.tags)
            self.assertTrue(any(t=="html" and a.get("lang")=="en-GB" for t,a in page.attrs))
            self.assertTrue(any(t=="meta" and a.get("name")=="viewport" for t,a in page.attrs))
            self.assertTrue(any(t=="meta" and a.get("name")=="description" for t,a in page.attrs))
            self.assertIn("Skip to content",(ROOT/name).read_text(encoding="utf-8"))
    def test_links_and_anchors(self):
        parsed=pages()
        for name,page in parsed.items():
            for link in page.links:
                value=urlparse(link)
                if value.scheme:
                    self.assertIn(value.scheme,{"https","mailto"})
                    continue
                target=value.path or name
                path=ROOT/unquote(target)
                self.assertTrue(path.is_file(),link)
                if value.fragment:
                    self.assertIn(value.fragment,parsed[target].ids,link)
    def test_policy_content_and_fifteen_sections(self):
        text=(ROOT/"privacy.html").read_text(encoding="utf-8")
        page=pages()["privacy.html"]
        self.assertEqual(15,len(re.findall(r'<section id=',text)))
        for value in ["The Art of Dining","Alexander Orekhov","Takoda Digital","Cyprus","takodadigital@gmail.com","com.takodadigital.theartofdining","SharedPreferences","Google Mobile Ads SDK","18 and over","does not show an in-app advertising consent form"]:self.assertIn(value,text)
        self.assertEqual(15,page.headings.count("h2")-1)
        self.assertIn("https://policies.google.com/privacy",page.links)
    def test_no_tracking_or_external_assets(self):
        for page in pages().values():
            self.assertEqual([],page.scripts)
            for tag,attrs in page.attrs:
                self.assertNotIn("src",attrs)
                self.assertNotEqual("form",tag)
                if tag=="link":self.assertFalse(urlparse(attrs.get("href","")).scheme)
        css=(ROOT/"assets/style.css").read_text(encoding="utf-8")
        self.assertNotIn("@import",css);self.assertNotIn("url(",css)
        self.assertIn("@media(max-width:600px)",css)
        self.assertIn(":focus-visible",css)
        self.assertEqual(css.count("{"),css.count("}"))
    def test_no_secrets_or_unresolved_site_placeholders(self):
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:continue
            self.assertNotIn(path.suffix.lower(),{".jks",".keystore",".aab",".apk",".p12"})
            if path.suffix in {".html",".css"}:
                text=path.read_text(encoding="utf-8")
                self.assertFalse(re.search(r"[\u0400-\u052f]",text))
                self.assertNotIn("GITHUB_USERNAME",text)
                self.assertNotIn("BEGIN PRIVATE KEY",text)
        self.assertTrue((ROOT/".nojekyll").is_file())

if __name__=="__main__":unittest.main()
