#!/usr/bin/env python

import os
import sys
import time
import httplib
import urllib
import socket
import urlparse
import httplib
import requests
import webbrowser
from lxml import html
from string import whitespace
from colorama import init , Style, Back,Fore
import mechanize
import thread
from  more_itertools import unique_everseen

#pip install -r requirements.txt

wrong_art = """

                    |'.             ,
                   |  '-._        / )
                 .'  .._  ',     /_'-,
                '   /  _'.'_\   /._)')
               :   /  '_' '_'  /  _.'
               |E |   |Q| |Q| /   /
              .'  _\  '-' '-'    /
            .'--.(S     ,__` )  /
                  '-.     _.'  /
                __.--'----(   /
            _.-'     :   __\ /
           (      __.' :'  :Y
            '.   '._,  :   :|
              '.     ) :.__:|
                \    \______/
                 '._L/_H____]
                  /_        /
                 /  '-.__.-')
                :      /   /
                :     /   /
              ,/_____/----;
              '._____)----'
              /     /   /
             /     /   /
           .'     /    \


"""

print wrong_art
print("[+] "+Fore.GREEN+"420.py - created by @int0x33 \n\n\n\n"+Style.RESET_ALL)

def get_page_urls(tree):
    siteurls = tree.xpath("//a/@href")
    return siteurls

def get_all_forms(tree):
    methods = tree.xpath("//form/@method")
    return methods

def form_action(tree, formnumber):
    action = tree.xpath("//form["+str(formnumber)+"]/@action")
    return action

def form_method(tree, formnumber):
    method = tree.xpath("//form["+str(formnumber)+"]/@method")
    return method

def form_query_strings(tree, formnumber):
    querystrings = tree.xpath("//form["+str(formnumber)+"]//input/@name")
    return querystrings

def spider(url):
    try:
        urls = []
        posturls = []
        requesturl = 'http://'+url
        page = requests.get(requesturl)
        tree = html.fromstring(page.content)

        methods = get_all_forms(tree)
        pageurls = get_page_urls(tree)

        formnumber = 1
        for method in methods:
            action = form_action(tree, formnumber)
            formmethod = form_method(tree, formnumber)
            sys.stdout.flush()
            print(Style.BRIGHT+Fore.RED+"[+] FORM FOUND on "+ url + " (" + formmethod[0].lower() + ")" +Style.RESET_ALL)
            if action[0].find(url) == -1:
                newurl = requesturl + action[0] + "?"
            else:
                url = action[0] + "?"
                newurl = url.replace("//", "")
            querystrings = form_query_strings(tree, formnumber)
            formnumber += 1
            for query in list(unique_everseen(querystrings)):
                newurl += query + "=&"
            cleanurl = newurl.replace("https://","").replace("http://","").replace("www.","").replace("http:","")
            #print newurl
            if formmethod[0].lower() == "get":
                urls.append("http://" + cleanurl)
            else:
                posturls.append("http://" + cleanurl)

        return (urls, posturls)

    except(KeyboardInterrupt) as Exit:
        print("\nExit...")
        sys.exit(1)
    except:
        print "[!] Something went wrong!"
        return ([], [])

def printbanner(p,status):
	try:
		b = ""
		l = ""
		lostatus = ""
		num = []
		s = len(max(p, key=len)) #list
		if s < 10:
			s = 10
		for i in range(len(p)): num.append(i)
		maxval = str(len(num)) #number
		for i in range(s) : b = b + "-"
		for i in range(len(maxval)):l = l + "-"
		statuslen = len(max(status, key=len))
		for i in range(statuslen) : lostatus = lostatus + "-"
		if len(b) < 10 :
			b = "----------"
		if len(lostatus) < 14:
			lostatus="--------------"
		if len(l) < 2 :
			l = "--"
		los = statuslen
		if los < 14:
			los = 14
		lenb=len(str(len(b)))
		if lenb < 14:
			lenb = 10
		else:
			lenb = 20
		upb = ("+-%s-+-%s-+-%s-+")%(l,b,lostatus)
		print(upb)
		st0 = "Parameters"
		st1 = "Status"
		print("| Id | "+st0.center(s," ")+" | "+st1.center(los," ")+" |")
		print(upb)
		for n,i,d in zip(num,p,status):
		    string = (" %s | %s ")%(str(n),str(i));
		    lofnum = str(n).center(int(len(l))," ")
		    lofstr = i.center(s," ")
		    lofst = d.center(los," ")
		    if "Not Vulnerable" in lofst:
		    	lofst = Fore.GREEN+d.center(los," ")+Style.RESET_ALL
		    else:
		    	lofst = Fore.RED+d.center(los," ")+Style.RESET_ALL
		    print("| "+lofnum+" | "+lofstr+" | "+lofst+" |")
		    print(upb)
		return("")
	except(ValueError):
		print(Style.BRIGHT+Fore.RED+"[!] Uh oh! No parameters in URL!"+Style.RESET_ALL)
		#again()

def complete(p,r,c,d):
	print("[+] 420 scan for "+d+" is complete!")
	if c == 0:
		print("[+] Given parameters are "+Style.BRIGHT+Fore.GREEN+"not vulnerable"+Style.RESET_ALL+" to XSS.")
	elif c ==1:
		print("[+] %s Parameter is "+Style.BRIGHT+Fore.RED+"vulnerable"+Style.RESET_ALL+" to XSS.")%c
	else:
		print("[+] %s Parameters are "+Style.BRIGHT+Fore.RED+"vulnerable"+Style.RESET_ALL+" to XSS.")%c
	print("[+] Scan Result for %s:")%d
	print printbanner(p,r)
	#again()

def wordlistimport(file,lst):
	try:
		with open(file,'r') as f: #Importing Payloads from specified wordlist.
			#print(Style.DIM+Fore.WHITE+"[+] Loading Payloads..."+Style.RESET_ALL)
			for line in f:
				final = str(line.replace("\n",""))
				lst.append(final)
	except IOError:
		print(Style.BRIGHT+Fore.RED+"[!] Wordlist not found!"+Style.RESET_ALL)
		#again()

def pwn(url):
    try:
        grey = Style.DIM+Fore.WHITE
        finalurl = urlparse.urlparse(url)
        urldata = urlparse.parse_qsl(finalurl.query)
        domain0 = '{uri.scheme}://{uri.netloc}/'.format(uri=finalurl)
        domain = domain0.replace("https://","").replace("http://","").replace("www.","").replace("/","").replace("https:","").replace("http:","")
        print (Style.DIM+Fore.WHITE+"[+] testing connection to "+domain+"..."+Style.RESET_ALL)
        try:
            connection = httplib.HTTPConnection(domain)
            connection.connect()
            print("[+] "+Fore.GREEN+domain+" connection established!"+Style.RESET_ALL)
            site = url
            paraname = []
            paravalue = []
            wordlist = 'wordlist_test.txt'
            payloads = []
            wordlistimport(wordlist,payloads)
            lop = str(len(payloads))
            grey = Style.DIM+Fore.WHITE
            #print(Style.DIM+Fore.WHITE+"[+] "+lop+" Payloads Loaded"+Style.RESET_ALL)
            print("[+] Running GET test on "+site)
            o = urlparse.urlparse(site)
            parameters = urlparse.parse_qs(o.query,keep_blank_values=True)
            path = urlparse.urlparse(site).scheme+"://"+urlparse.urlparse(site).netloc+urlparse.urlparse(site).path
            for para in parameters: #Arranging parameters and values.
                for i in parameters[para]:
                    paraname.append(para)
                    paravalue.append(i)
            total = 0
            c = 0
            fpar = []
            fresult = []
            progress = 0
            for pn, pv in zip(paraname,paravalue): #Scanning the parameter.
                #print(grey+"[+] Testing '"+pn+"' parameter..."+Style.RESET_ALL)
                fpar.append(str(pn))
                try:
                    for x in payloads: #
                        validate = x.translate(None, whitespace)
                        if validate == "":
                            progress = progress + 1
                        else:
                            #sys.stdout.write("\r[+] %i / %s payloads injected..."% (progress,len(payloads)))
                            #sys.stdout.flush()
                            progress = progress + 1
                            enc = urllib.quote_plus(x)
                            data = path+"?"+pn+"="+pv+enc
                            try:
                                page = urllib.urlopen(data)
                                sourcecode = page.read()
                                if x in sourcecode:
                                    print(Style.BRIGHT+Fore.RED+"\n[!]"+" XSS Vulnerability Found! \n"+Fore.RED+Style.BRIGHT+"[!]"+" Parameter:\t%s\n"+Fore.RED+Style.BRIGHT+"[!]"+" Payload:\t%s"+Style.RESET_ALL)%(pn,x)
                                    webbrowser.open(data, new=0, autoraise=True)
                                    fresult.append("  Vulnerable  ")
                                    c = 1
                                    total = total+1
                                    progress = progress + 1
                                    break
                                else:
                                    c = 0
                            except(KeyboardInterrupt) as Exit:
                        		print("\nExit...")
                        		sys.exit(1)
                            except:
                                "Connection issue!"
                except(KeyboardInterrupt) as Exit:
                    print("\nExit...")

                if c == 0:
                    #print(Style.BRIGHT+Fore.GREEN+"\n[+]"+Style.RESET_ALL+Style.DIM+Fore.WHITE+" '%s' parameter not vulnerable."+Style.RESET_ALL)%pn
                    fresult.append("Not Vulnerable")
                    progress = progress + 1
                    pass
                progress = 0
            complete(fpar,fresult,total,domain)
        except(httplib.HTTPResponse, socket.error) as Exit:
            print(Style.BRIGHT+Fore.RED+"[!] Site "+domain+" is offline!"+Style.RESET_ALL)
            #again()
    except:
        print(Style.BRIGHT+Fore.RED+"[!] Connection Error! Might be 404, firewall or no socket"+Style.RESET_ALL)

def pwnpost(url):
    try:
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')]
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        finalurl = urlparse.urlparse(url)
        urldata = urlparse.parse_qsl(finalurl.query)
        domain0 = '{uri.scheme}://{uri.netloc}/'.format(uri=finalurl)
        domain = domain0.replace("https://","").replace("http://","").replace("www.","").replace("/","").replace("https:","").replace("http:","")
        print (Style.DIM+Fore.WHITE+"[+] testing connection to "+domain+"..."+Style.RESET_ALL)
        try:
            connection = httplib.HTTPConnection(domain)
            connection.connect()
            print("[+] "+Fore.GREEN+domain+" connection established!"+Style.RESET_ALL)
            path = urlparse.urlparse(url).scheme+"://"+urlparse.urlparse(url).netloc+urlparse.urlparse(url).path
            postdata = url.split('?')
            param = postdata[1]
            #param = str(raw_input("[?] Enter post data: > "))
            wordlist = 'wordlist.txt'
            payloads = []
            wordlistimport(wordlist,payloads)
            lop = str(len(payloads))
            grey = Style.DIM+Fore.WHITE
            print(Style.DIM+Fore.WHITE+"[+] "+lop+" Payloads Loaded"+Style.RESET_ALL)
            print("[+] POST test:")
            params = postdata[0] + "?"+param
            finalurl = urlparse.urlparse(params)
            urldata = urlparse.parse_qsl(finalurl.query)
            o = urlparse.urlparse(params)
            parameters = urlparse.parse_qs(o.query,keep_blank_values=True)
            paraname = []
            paravalue = []
            for para in parameters: #Arranging parameters and values.
                for i in parameters[para]:
                    paraname.append(para)
                    paravalue.append(i)
            fpar = []
            fresult = []
            total = 0
            progress = 0
            pname1 = [] #parameter name
            payload1 = []
            for pn, pv in zip(paraname,paravalue): #Scanning the parameter.
                #print(grey+"[+] Testing '"+pn+"' parameter..."+Style.RESET_ALL)
                fpar.append(str(pn))
                try:
                    for i in payloads:
                        validate = i.translate(None, whitespace)
                        if validate == "":
                            progress = progress + 1
                        else:
                            progress = progress + 1
                            #sys.stdout.write("\r[+] %i / %s payloads injected..."% (progress,len(payloads)))
                            #sys.stdout.flush()
                            pname1.append(pn)
                            payload1.append(str(i))
                            d4rk = 0
                            for m in range(len(paraname)):
                                d = paraname[d4rk]
                                d1 = paravalue[d4rk]
                                tst= "".join(pname1)
                                tst1 = "".join(d)
                                if pn in d:
                                    d4rk = d4rk + 1
                                else:
                                    d4rk = d4rk +1
                                    pname1.append(str(d))
                                    payload1.append(str(d1))
                            data = urllib.urlencode(dict(zip(pname1,payload1)))
                            r = br.open(path, data)
                            sourcecode =  r.read()
                            pname1 = []
                            payload1 = []
                            if i in sourcecode:
                                print(Style.BRIGHT+Fore.RED+"\n[!]"+" XSS Vulnerability Found! \n"+Fore.RED+Style.BRIGHT+"[!]"+" Parameter:\t%s\n"+Fore.RED+Style.BRIGHT+"[!]"+" Payload:\t%s"+Style.RESET_ALL)%(pn,i)
                                fresult.append("  Vulnerable  ")
                                webbrowser.open(data, new=0, autoraise=True)
                                c = 1
                                total = total+1
                                progress = progress + 1
                                break
                            else:
                                c = 0
                except(KeyboardInterrupt) as Exit:
                	print("\nExit...")

                if c == 0:
                    #print(Style.BRIGHT+Fore.GREEN+"\n[+]"+Style.RESET_ALL+Style.DIM+Fore.WHITE+" '%s' parameter not vulnerable."+Style.RESET_ALL)%pn
                    fresult.append("Not Vulnerable")
                    progress = progress + 1
                    pass
                progress = 0
            complete(fpar,fresult,total,domain)
        except(httplib.HTTPResponse, socket.error) as Exit:
            print(Style.BRIGHT+Fore.RED+"[!] Site "+domain+" is offline!"+Style.RESET_ALL)
            #again()
        except(KeyboardInterrupt) as Exit:
    		print("\nExit...")
    except:
        print(Style.BRIGHT+Fore.RED+"[!] Connection Error! Might be 404, firewall or no socket"+Style.RESET_ALL)

def pwn420():
    qbfile = open(sys.argv[1],"r")
    linenumber = 0
    for aline in qbfile.readlines():
        if linenumber < 1:
            linenumber+=1
            values = aline.split()
            urls = spider(values[0])
            print "[x] Checking "+values[0]
        else:
            for url in list(unique_everseen(urls[0])):
                thread.start_new_thread( pwn, (url,) )
                #pwn(url)
            #for url in list(unique_everseen(urls[1])):
                #pwnpost(url)
                #thread.start_new_thread( pwnpost, (url,) )
            linenumber = 0
            formnumber = 0
            urls = []
            posturls = []
    qbfile.close()

pwn420()
