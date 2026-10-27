"""Two-sided US-letter roll-fold brochure; content extracted from the website."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
class Node:
 def __init__(self,tag='',attrs=()):self.tag=tag;self.attrs=dict(attrs);self.children=[]
 def text(self):return ' '.join(' '.join(c.text() if isinstance(c,Node) else c for c in self.children).split())
 def walk(self):
  yield self
  for c in self.children:
   if isinstance(c,Node):yield from c.walk()
 def find(self,tag=None,id=None,cls=None):
  return next((n for n in self.walk() if (not tag or n.tag==tag) and (not id or n.attrs.get('id')==id) and (not cls or cls in n.attrs.get('class','').split())),None)
 def all(self,tag):return [n for n in self.walk() if n.tag==tag]
class Tree(HTMLParser):
 def __init__(self):super().__init__();self.root=Node();self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in ('br','img','meta','link','input','hr','source'):self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].children.append(s)
t=Tree();t.feed((ROOT/'dist/index.html').read_text());site=t.root
assets=ROOT/'dist/assets';photos=ROOT/'brochure-assets'
for name,file in [('Source','source-sans-3-400.ttf'),('SourceBold','source-sans-3-700.ttf'),('Lora','lora-600.ttf')]:pdfmetrics.registerFont(TTFont(name,str(assets/file)))
pdfmetrics.registerFontFamily('Source',normal='Source',bold='SourceBold',italic='Source',boldItalic='SourceBold')
NAVY='#202c67';INK='#18224b';BODY='#596076';RED='#b23239';PALE='#f0f3f9';CREAM='#f7f5f1';LINE='#dce1ed'
W,H=792,612
out=assets/'vista-brochure.pdf';c=canvas.Canvas(str(out),pagesize=(W,H))
c.setTitle('Vista Home Health Services | Tri-fold brochure');c.setAuthor('Vista Home Health Services')
def rect(x,top,w,h,color):c.setFillColor(HexColor(color));c.rect(x,H-top-h,w,h,stroke=0,fill=1)
def para(text,x,top,w,size=10,leading=13,font='Source',color=BODY,markup=False):
 text=text.replace('–','-').replace('—','-')
 p=Paragraph(text if markup else escape(text).replace('\n','<br/>'),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=HexColor(color),spaceAfter=0))
 _,h=p.wrap(w,H)
 assert top+h<=H-14,(text[:55],top,h)
 p.drawOn(c,x,H-top-h);return top+h
def label(text,x,top,w,color=RED):return para(text.upper(),x,top,w,8,11,'SourceBold',color)
def heading(text,x,top,w,size=21,color=NAVY):return para(text,x,top,w,size,size*1.18,'Lora',color)
def photo(file,x,top,w,h,center=.5):
 im=Image.open(file);iw,ih=im.size;scale=max(w/iw,h/ih);dw,dh=iw*scale,ih*scale
 c.saveState();path=c.beginPath();path.rect(x,H-top-h,w,h);c.clipPath(path,stroke=0,fill=0)
 c.drawImage(str(file),x-(dw-w)*center,H-top-h-(dh-h)*.5,dw,dh,mask='auto');c.restoreState()
def rule(x,top,w):rect(x,top,w,0.7,LINE)
def listitems(items,x,top,w,size=10,bold=False,gap=6,color=BODY):
 for text in items:
  c.setFillColor(HexColor(RED));c.circle(x+2,H-top-6,1.5,stroke=0,fill=1)
  top=para(text,x+12,top,w-12,size,size*1.3,'SourceBold' if bold else 'Source',color)+gap
 return top
areas=[n.text() for n in site.find(cls='contact-areas').all('li')]
about=site.find(id='about');aboutcopy=[n for n in about.children if isinstance(n,Node)][-1].find(tag='p').text()
quote=' '.join(ch for ch in about.find(tag='blockquote').children if isinstance(ch,str)).strip('“” ')
coord=site.find(cls='coordination').all('p')[-1].text()
answer=site.find(cls='contact-intro').all('p')[-1].text()

# OUTSIDE: shorter fold-in flap / back panel / front cover.
rect(0,0,258,H,CREAM);rect(258,0,267,H,'#ffffff');rect(525,0,267,H,'#ffffff')
label('Our approach',22,32,214)
heading(about.find(tag='h2').text(),22,62,210,22)
photo(photos/'caregiver-support.jpg',22,173,214,160,.35)
para(aboutcopy,22,355,214,9.4,12.5)
rect(22,478,3,85,RED)
para('“'+quote+'”',36,479,196,10,14,'SourceBold',NAVY)
para('The home health service with a heart.',22,580,214,8,11,'SourceBold',RED)

x=282;cw=219
label('Contact Vista',x,32,cw)
heading('Let’s talk about\nyour care.',x,60,cw,23)
para('(661) 267-0097',x,135,cw,21,25,'SourceBold',NAVY)
label('Service areas',x,185,cw)
listitems(areas,x,208,cw,11,True,7,NAVY)
rule(x,339,cw)
para('Antelope Valley office',x,354,cw,10,14,'SourceBold',NAVY)
para('1543 E. Palmdale Blvd., Suite A\nPalmdale, CA 93550',x,375,cw,10,14)
para('Service hours',x,419,cw,10,14,'SourceBold',NAVY)
para('Monday-Friday: 8:30 a.m.-5:00 p.m.',x,439,cw,9.5,13)
para('Fax: (661) 267-0096',x,468,cw,9.5,13)
para(answer,x,505,cw,10,14)
para('vistahomehealthservices.com',x,579,cw,9.1,12,'SourceBold',NAVY)

c.drawImage(str(assets/'vista-logo.png'),547,H-97,223,223*725/2170,mask='auto')
photo(photos/'home-rehabilitation.jpg',525,112,267,252,.35)
rect(525,364,267,248,NAVY);rect(525,364,267,4,RED)
heading('Expert care.\nThe comfort\nof home.',548,390,220,27,'#ffffff')
para(site.find(cls='intro').text(),548,502,219,10.5,14,color='#ffffff')
para('VISTA HOME HEALTH SERVICES',548,583,219,8,11,'SourceBold','#ffffff')
c.showPage()

# INSIDE: clinical care / rehabilitation / coordinated support.
rect(0,0,267,H,'#ffffff');rect(267,0,267,H,PALE);rect(534,0,258,H,'#ffffff')
x=22;cw=223
label('Care & services',x,29,cw)
heading('Skilled nursing &\ndisease management',x,55,cw,20)
nursing=site.find(id='nursing');para(nursing.find(cls='detail-body').find(tag='p').text(),x,121,cw,9.5,12.5)
end=listitems([n.text() for n in nursing.all('li')],x,221,cw,9.4,False,4)
lab=site.find(id='laboratory');heading(lab.find(tag='strong').text(),x,end+12,cw,15)
end=para(lab.find(cls='detail-body').text(),x,end+38,cw,9.5,12.5)
rect(x,581,cw,2,RED)

x=289;cw=223
label('Home rehabilitation',x,29,cw)
heading('Help with everyday\nindependence.',x,55,cw,20)
photo(photos/'home-rehabilitation.jpg',x,120,cw,125,.35)
rehab=site.find(id='rehabilitation')
top=para(rehab.find(cls='detail-body').find(tag='p').text(),x,265,cw,9.4,12.5)+14
therapy=rehab.find(cls='therapy')
for n in therapy.children:
 if not isinstance(n,Node):continue
 if n.tag=='h3':top=para(n.text(),x,top,cw,10,13,'SourceBold',NAVY)+5
 elif n.tag=='p':top=para(n.text(),x,top,cw,9.4,12.5)+13
social=site.find(id='social');heading(social.find(tag='strong').text(),x,top,cw,15)
para(social.find(cls='detail-body').text(),x,top+28,cw,9.4,12.5)

x=556;cw=214
label('Everyday support',x,29,cw)
aides=site.find(id='aides');heading(aides.find(tag='strong').text(),x,55,cw,20)
para(aides.find(cls='detail-body').text(),x,94,cw,9.5,12.5)
heading('Coordinated care.',x,191,cw,20)
para(coord,x,229,cw,9.5,12.5)
heading('Getting started',x,319,cw,20)
steps=site.find(id='getting-started').all('article');top=365
for i,step in enumerate(steps,1):
 para(f'0{i}',x,top,25,10,13,'SourceBold',RED)
 top=para(step.find(tag='h3').text(),x+31,top,cw-31,10,13,'SourceBold',NAVY)+5
 top=para(step.find(tag='p').text(),x+31,top,cw-31,9.4,12.5)+17
rect(x,581,cw,2,RED)
c.save()
print(out)
