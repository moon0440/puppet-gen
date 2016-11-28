import sys, re

import xml.etree.ElementTree as etree
from mako.template import Template



def interface(vul_id,cc,rule_name,title,desc,fix_text,cci):
	print("="*100)
	print(("Vul ID:\n{0}\n").format(commentFormat(vul_id)))
	print(("Title:\n{0}\n").format(commentFormat(title)))
	print(("Check Content:\n{0}\n").format(commentFormat(cc)))
	print(("Fix Text:\n{0}\n").format(commentFormat(fix_text)))

	r = input("Type of puppet resouce->\n([1]augeas,[2]service,[3]package,[4]SKIP):")
	if r == 1:
		print("augeas setup")
	elif r == 2:
		print("service setup")
	elif r == 3:
		print("package setup")
	elif r == 4:
		print("Skip setup")
		return
	else:
		interface(vul_id,cc,rule_name,title,desc,fix_text,cci)

	return

def commentFormat(s):
	if re.search("^",s,re.MULTILINE):
		r = re.compile("^",re.MULTILINE)
		s = r.sub("\t|\t", s)
	return(s)

def main():
	root = etree.parse('U_Red_Hat_Enterprise_Linux_7_STIG_V1R0-2_Manual-xccdf.xml').getroot()
	namespace = "{http://checklists.nist.gov/xccdf/1.1}"
	tpp = Template(filename='template.pp')

	for g in root.findall("{0}Group".format(namespace)):
		vul_id = g.attrib['id']
		cc = g.find("./{0}Rule/{0}check/{0}check-content".format(namespace)).text
		rule_name = g.find("./{0}Rule".format(namespace))[0].text
		title = g.find("./{0}Rule/{0}title".format(namespace)).text
		#gen_info = g.find("./{0}Rule/{0}check/{0}check-content".format(namespace)).text
		desc = g.find("./{0}Rule/{0}description".format(namespace)).text
		fix_text = g.find("./{0}Rule/{0}fixtext".format(namespace)).text
		cci = g.find("./{0}Rule/{0}check/{0}check-content".format(namespace)).text
		doc = tpp.render(vul_id=vul_id,cc=cc,rule_name=rule_name,title=title,desc=desc,fix_text=fix_text,cci=cci)
		interface(vul_id=vul_id,cc=cc,rule_name=rule_name,title=title,desc=desc,fix_text=fix_text,cci=cci)
		print(doc)
		sys.exit()


if __name__ == "__main__":
	main()
