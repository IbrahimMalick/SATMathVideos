---
scene: cs.internet
---

<!-- Cambridge O Level 2210 Chapter 5: The Internet and Its Uses. Anchors copied from the transcript, mis-hearings and all. -->

[[beat:open]] Chapter 5. The Internet and its Users. [[beat:welcome]] Welcome to
Chapter 5 of Cambridge O 'Level Computer Science 2210. In this lesson, we will
[[beat:journey_promise]] follow the journey from entering a web address to seeing a
page appear on screen. [[beat:also_cookies]] We will also look at cookies,
[[beat:also_threats]] digital currency, blockchain, common cybersecurity security
threats and [[beat:also_controls]] the controls that help protect users and computer
systems. As we go, [[beat:easy_to_confuse]] pay attention to the differences between
terms that are easy to confuse. In an exam answer, [[beat:naming_first_step]] naming
the correct term is only the first step. [[beat:explain_it]] You also need to explain
what it does. First [[beat:distinguish]] let's distinguish the internet from the world
wide web. [[beat:internet_is]] The internet is the global network infrastructure that
connects computers and other devices. [[beat:web_is]] The worldwide web is a
collection of websites and webpages that people access using the internet. The web
uses the internet but [[beat:not_the_same]] the two terms do not mean the same thing.
For example someone can [[beat:email_example]] use the internet to send email or play
an online game without viewing a web page. [[beat:browser_intro]] A web page is
usually accessed through a web browser. [[beat:browser_jobs]] A browser can request
web resources, interpret the code used to build a page, and display that page on the
screen. [[beat:browser_tools]] It also provides tools such as an address bar, tabs,
bookmarks, and browsing history. Now let's look at what happens when someone enters a
web address. [[beat:url_open]] A web address is called a URL which stands for Uniform
Resource locator. [[beat:url_parts]] A URL identifies a resource and can contain
several parts. [[beat:three_parts]] These may include a protocol, a domain name, and a
path to a particular page or file. For example, [[beat:protocol_is]] the protocol
tells the browser how to communicate with the web server. [[beat:domain_is]] The
domain name identifies the website the user wants to reach. [[beat:path_is]] The path
can identify a specific page or resource on that website. When a user enters a The
URL, [[beat:extract_domain]] the browser first extracts the domain name.
[[beat:needs_ip]] The browser needs the internet protocol address for the server
associated with that domain. [[beat:asks_dns]] It asks a domain name system server,
often called DNS, to resolve the domain name. [[beat:resolving_means]] Resolving means
finding the IP address associated with the domain. [[beat:dns_returns]] The DNS server
returns the address to the browser. [[beat:dns_not_page]] The DNS server does not
normally send the web page. [[beat:dns_job]] Its job is to help the browser find the
correct server. [[beat:connects]] The browser then connects to the web server at the
returned IP address. [[beat:sends_request]] It sends a request using HTTP or HTTPS.
[[beat:http_is]] HTTP is a protocol used to transfer web resources. [[beat:https_is]]
HTTPS uses secure communication to protect data traveling between the browser and the
web server. [[beat:server_returns]] The web server receives the request and returns
the requested resources. [[beat:what_comes_back]] These may include HTML code, images,
style information and other files needed to display the page. [[beat:renders]] The
browser interprets the HTML, retrieves any linked resources it needs and renders the
page on the screen. [[beat:recap_1]] So the process is the user enters a URL.
[[beat:recap_2]] The browser extracts the domain name. [[beat:recap_3]] DNS finds the
server's IP address. [[beat:recap_4]] The browser connects to the web server and sends
a request. [[beat:recap_5]] The server returns the requested resources.
[[beat:recap_6]] The browser interprets those resources and displays the page.
[[beat:distinction]] Keep one important distinction clear. [[beat:dns_does]] DNS
resolves the domain name to an IP address. [[beat:server_does]] The web server returns
the web page resources. [[beat:cookies_open]] Websites often need to remember
information about a user between requests. [[beat:cookie_is]] A cookie is a small
piece of data stored by the browser for a website. [[beat:cookies_convenient]] Cookies
can make a website more convenient. For example, [[beat:basket]] they may help a
shopping website remember the items in a user's basket. [[beat:preferences]] They can
also remember preferences or help maintain a user's login state. [[beat:two_types]]
There are two cookie types you need to distinguish. [[beat:named]] Session cookies and
persistent cookies. [[beat:session_is]] A session cookie normally remains only while
the current browser session is active. [[beat:session_deleted]] It may be deleted when
the user closes the browser or ends the session. [[beat:session_use]] A website might
use one to remember items in a shopping basket while the user moves between pages.
[[beat:persistent_is]] A persistent cookie remains after the browser is closed.
[[beat:persistent_until]] It is stored until it expires or is deleted.
[[beat:persistent_use]] A website might use one to remember a preference, a login
detail, or information used for long -term tracking. [[beat:privacy]] Cookies can
improve convenience, but they also raise privacy concerns. For example,
[[beat:tracking]] persistent cookies can be used to track a user's behavior over time.
When comparing these cookie types, [[beat:compare_cookies]] compare how long each one
lasts and how it may be used. [[beat:currency_open]] The internet also supports
digital currency. [[beat:currency_is]] Digital currency exists electronically and can
be transferred between digital wallets. [[beat:uses_blockchain]] Some digital
currencies use a blockchain to record transactions. [[beat:ledger]] A blockchain is a
digital ledger made up of linked records called blocks. [[beat:simplified]] Here is a
simplified explanation of how a blockchain transaction can be recorded.
[[beat:broadcast]] A transaction is requested and broadcast to computers participating
in the network. [[beat:network_checks]] The network checks whether the transaction
follows its agreed rules. [[beat:grouped]] Valid transactions are grouped into a
block. block. [[beat:timestamp_link]] The block includes a timestamp and a
cryptographic link to the previous block. [[beat:replicated]] When the network accepts
the block, it is added to replicated copies of the ledger. Because each block is
linked to the previous one, [[beat:changing_older]] changing an older record would
affect the links in later blocks. [[beat:needs_network]] An attacker would also need
the network to accept the altered record. [[beat:difficult]] This makes undetected
changes difficult. However, [[beat:not_impossible]] do not say that every blockchain
chain is completely impossible to attack. [[beat:accurate]] The accurate explanation
is that the linked records and network agreement make unauthorized changes difficult
to carry out without detection. [[beat:threats_open]] Now let's turn to cybersecurity
threats. [[beat:threat_is]] A cybersecurity threat is an action or piece of software
that can put data or systems at risk. [[beat:different_ways]] Different threats work
in different ways. [[beat:brute_force]] A brute force attack tries many possible
password combinations in an attempt to gain access to an account or system.
[[beat:interception]] Data interception happens when someone captures data while it is
being transmitted between devices. [[beat:hacking]] Hacking means gaining unauthorized
access to data or computer systems, [[beat:ddos]] a distributed denial of service
attack, or DDoS attack, [[beat:ddos_flood]] uses many devices to flood a service with
traffic. [[beat:ddos_aim]] The aim is to make that service slow or unavailable to its
intended users. Notice the aim of a DDOS attack. [[beat:availability]] It targets
availability. [[beat:malware_open]] Malware is malicious software.
[[beat:malware_types]] There are several different types of malware. [[beat:virus]] A
virus attaches itself to a file or program and can spread when the infected file is
executed. [[beat:worm]] A worm can copy itself and spread across networks without
needing to attach itself to another file in the same way. [[beat:trojan]] A Trojan
horse appears legitimate or useful but performs malicious actions once installed or
run. [[beat:spyware]] Spyware secretly records activity or collects information from a
user's device. [[beat:adware]] Adware displays unwanted advertising and may also track
a user's behavior. [[beat:ransomware]] Ransomware encrypts or locks data and demands
payment to restore access. [[beat:mechanisms]] These terms describe different
mechanisms. [[beat:virus_host]] A virus needs a host file and usually relies on
execution by a user. [[beat:worm_self]] A worm can self -replicate across a network.
[[beat:trojan_deceives]] A Trojan horse deceives the user about what the software
does. [[beat:ransomware_blocks]] Ransomware prevents access to data and demands
payment. [[beat:spyware_collects]] Spyware secretly collects information.
[[beat:too_vague]] Calling all of these threats a virus is too vague. [[beat:name_it]]
Name this specific threat and explain how it works. [[beat:deceive_open]] Some attacks
focus on deceiving people. [[beat:phishing_is]] Fishing uses a fraudulent message to
trick someone into revealing information or taking an unsafe action. For example,
[[beat:phishing_bank]] a message might pretend to come from a bank and ask the user to
confirm account details. [[beat:phishing_link]] The message may include a link to a
fake website designed to collect the user's login information. [[beat:pharming_is]]
Farming is different. [[beat:pharming_how]] It redirects the user to a fake website
even when the user enters the correct URL. [[beat:pharming_cause]] The redirection may
be caused by malicious code on the user's computer or by a compromised DNS server.
[[beat:keep_clear]] Keep the distinction clear. [[beat:phishing_short]] Fishing users
a deceptive message to persuade the user to act. [[beat:pharming_short]] Farming
redirects the user to a fake destination. [[beat:social_is]] Social engineering is the
broader practice of manipulating people into weakening security. [[beat:pretend]] An
attacker may pretend to be a colleague, a technician, or an official representative.
[[beat:social_aim]] The attacker's aim might be to persuade someone to reveal a
password, approve a request, or open a harmful attachment. [[beat:not_only_software]]
Security is not only about software and devices, [[beat:people_decide]] people's
decisions also affect security. [[beat:controls_open]] Let's match security controls
to the threats they can reduce. [[beat:authentication]] Authentication checks that a
user is who they claim to be. [[beat:auth_kinds]] It may use a password, a biometric
check, or two -step verification. Two -step [[beat:two_step]] verification requires an
additional check after the password. For example, [[beat:code_to_device]] a user may
need to enter a code sent to a separate device. [[beat:stolen_password]] This can
reduce the risk of someone accessing an account using a stolen password alone.
[[beat:access_levels]] Access levels limit which resources each user can use. For
example, [[beat:student_account]] a student account may be allowed to view a file but
not change the school system settings. [[beat:firewall]] A firewall filters network
traffic according to a set of rules. It can block some unwanted connections,
[[beat:firewall_limits]] although it cannot prevent every type of attack. Anti
-malware [[beat:antimalware]] software can detect, quarantine, and remove known
malicious software. [[beat:updates]] Automatic updates install fixes for known
vulnerabilities. Its [[beat:updates_why]] keeping software updated can reduce the
chance that an attacker will exploit an existing weakness and Christian
[[beat:encryption]] protects data as it travels between devices. [[beat:https_again]]
HTTPS uses secure communication based on encryption and server authentication.
[[beat:certificate]] A valid security certificate can help the browser verify the
identity of the server. [[beat:https_limit]] But HTTPS does not prove that every claim
on a website is trustworthy. [[beat:fake_still_lies]] A fake website can still make
false claims, even if its connection is encrypted. [[beat:proxy]] A proxy server acts
as an intermediary between a user and other servers. [[beat:proxy_does]] It can filter
requests or help hide the internal addresses of devices on a network.
[[beat:privacy_settings]] Privacy settings can limit the personal information that a
user shares. [[beat:check_message]] Users can also check the sender, wording, and
destination of a suspicious message. [[beat:check_link]] Before entering bank details,
they should check whether a link leads to the genuine website. [[beat:no_single]] No
single security control stops every threat. [[beat:layers]] security is strongest when
several controls work together. [[beat:example_open]] Let's apply these ideas to a
message asking for bank details. [[beat:check_sender]] First, check who sent it.
[[beat:sender_address]] Look carefully at the sender's address and ask whether the
request is expected. [[beat:check_wording]] Next, check the wording.
[[beat:wording_signs]] Poor spelling, a threatening tone or an urgent demand may
indicate a suspicious message. [[beat:check_destination]] Then inspect the destination
of any link before opening it. [[beat:text_vs_address]] The visible text may not match
the actual website address. Even if the message looks convincing,
[[beat:do_not_enter]] do not enter private details through an unexpected link.
Instead, [[beat:contact_directly]] contact the bank using a trusted phone number or by
opening its known website directly. Two -step [[beat:two_step_helps]] verification can
provide extra protection if a password is stolen. However, [[beat:but_not_the_code]]
it cannot make it safe to give a verification code to an attacker.
[[beat:both_matter]] Technical controls matter and careful user behavior matters too.
[[beat:recap_open]] Let's finish with the main ideas from this chapter.
[[beat:r_internet]] The Internet is the network infrastructure. [[beat:r_web]] The
World Wide Web is a collection of web pages and websites accessed through that
infrastructure. When a user enters a URL [[beat:r_dns]] DNS resolves the domain name
to an IP address. [[beat:r_browser]] The browser connects to the web server, requests
resources and renders the return page. Session cookies and [[beat:r_cookies]]
persistent cookies differ mainly in how long they remain stored. [[beat:r_blockchain]]
A blockchain is a linked timestamp digital ledger that is difficult to alter without
detection. [[beat:r_threats]] Cybersecurity threats use different methods.
[[beat:r_virus]] A virus attaches to a host file. [[beat:r_worm]] A worm can self
-replicate across networks. [[beat:r_phishing]] Fishing uses deceptive messages, while
farming redirects a user to a fake website. [[beat:r_ddos]] A DDOS attack aims to make
a service unavailable. [[beat:r_ransomware]] Ransomware locks or encrypts data and
demands payment. [[beat:r_layers]] Security works best in layers, [[beat:r_controls]]
authentication, access levels, firewalls, anti -malware, updates, encryption, privacy
settings and informed user decisions. [[beat:r_each]] each help reduce different
risks. When answering exam questions, [[beat:exam_advice]] identify the threat or
technology precisely, describe how it works, and [[beat:connect_control]] connect the
security control to the risk it reduces. [[beat:close]] That is the key to writing
clear, well -supported answers for Chapter 5.
