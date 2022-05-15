import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen

headers = {
    "User-Agent": "my practice web program for an herbal class project. I can be contacted at lrkdxn@gmail.com"
}

yellow = 'http://slavekiten.tripod.com/id20.html'
alternate = 'https://www.themagickalcat.com/Articles.asp?ID=242'

sauce = urlopen(yellow)
webPage = sauce.read()
soup = BeautifulSoup(webPage, "html.parser")

h3 = soup.find_all('h3')
attribute = h3[-1]
astrosign = h3[2]
element = h3[1]
planetary = h3[0]


def gather_section(section_title):
    body = section_title.parent.parent.find('tbody')
    section = body.find_all('tr')
    # print (section)
    return section

def parse_section(topic):
    parent_list = []
    herb_lists = []

    for parsed in topic:
        parent_cell = parsed.findNext('td')

        if parent_cell != None  :
            parented = parent_cell.text
            parent = str(parented)
            parent_list.append(parent)

            dependent_cell = parent_cell.findNext('td')
            dependents = dependent_cell.text                
            herbs = dependents.split(',')

            herbslist = []                
            i = 0
            while i < len(herbs):
                herb = herbs[i].strip()
                herb_str = str(herb)
                herbslist.append(herb_str)
                
                i = i + 1
            # print herbslist
            herb_lists.append(herbslist)

    inserts = {}
    p = 0
    for k in parent_list:
        print (k)
        insert = {parent_list[p] : herb_lists[p]}
        inserts.update(insert)
        p = p + 1
    return inserts
        

new = eval(input('choose correspondence: \n *astrosign \n *element \n *attribute \n *planetary \n'))

section = gather_section(new)
breakdown =parse_section(section)   
# print (breakdown)

for key in breakdown:
    print (key, ': ', breakdown[key])
    print('------------------------------------------------------------------')

