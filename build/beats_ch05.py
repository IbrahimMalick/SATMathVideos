"""Beat placement for Chapter 5, The Internet and Its Uses -- 2210.

Run from the repo root:

    python build/beats_ch05.py

The narration is an ElevenLabs reading of the script, not a recording of
a person, and it needed no preparation at all:

    python build/transcribe.py audio/CH05-internet.mp3 \\
        --model small --language en

No dead air at either end, and no digital-silence false start of the
kind the Part 1 reading had, where the voice began, stopped dead for 1.6
seconds of exact zeros and started again. That one had to be cut with
ffmpeg before anything else could happen; this one is clean from the
first sample to the last. ``find_loops`` reports nothing either.

The transcriber, though, mis-heard a good deal of correct audio, and the
anchors below are copied from what it produced rather than from the
script -- "Fishing" for phishing, "Farming" for pharming, and best of
all "and Christian protects data as it travels between devices" for
"Encryption protects data". Every caption on screen carries the real
word. The anchors cannot, because an anchor is matched against the
transcript: a phrase corrected to the script is not in the file, and
would either fail to match or, far worse, match somewhere it should not.

Two of those are worth checking rather than assuming. The opening reads
"The Internet and its Users" where the title is "Uses"; re-transcribing
the first five seconds with the medium model gives "Uses", so the audio
is right and the small model simply misheard. The screen says "Uses".
"""

from mkbeats import build

BEATS = [
    # ------------------------------------------------------- 1. opening
    ("open", "Chapter 5. The Internet and its"),
    ("welcome", "Welcome to Chapter 5 of Cambridge"),
    ("journey_promise", "follow the journey from entering a web address"),
    ("also_cookies", "We will also look at cookies"),
    ("also_threats", "digital currency, blockchain, common cybersecurity"),
    ("also_controls", "the controls that help protect users and computer"),
    ("easy_to_confuse", "pay attention to the differences between terms"),
    ("naming_first_step", "naming the correct term is only the first"),
    ("explain_it", "You also need to explain what it does"),

    # --------------------------------------- 2. the internet and the web
    ("distinguish", "let's distinguish the internet from the world wide web"),
    ("internet_is", "The internet is the global network infrastructure"),
    ("web_is", "The worldwide web is a collection of websites"),
    ("not_the_same", "the two terms do not mean the same thing"),
    ("email_example", "use the internet to send email or play an online game"),
    ("browser_intro", "A web page is usually"),
    ("browser_jobs", "A browser can request web resources, interpret the code"),
    ("browser_tools", "It also provides tools such as an address bar, tabs"),

    # ------------------------------------------------------ 3. the URL
    ("url_open", "A web address is called a URL which stands for Uniform"),
    ("url_parts", "A URL identifies a resource and can contain several parts"),
    ("three_parts", "These may include a protocol, a domain name, and a path"),
    ("protocol_is", "the protocol tells the browser how to communicate"),
    ("domain_is", "The domain name identifies"),
    ("path_is", "The path can identify a specific page or resource"),

    # ---------------------------------------------- 4. URL to page on screen
    ("extract_domain", "the browser first extracts the domain name"),
    ("needs_ip", "The browser needs the internet protocol address"),
    ("asks_dns", "It asks a domain name system server, often called DNS"),
    ("resolving_means", "Resolving means finding the"),
    ("dns_returns", "The DNS server returns the address to the browser"),
    ("dns_not_page", "The DNS server does not normally send"),
    ("dns_job", "Its job is to help the browser find the correct server"),
    ("connects", "The browser then connects to the web server"),
    ("sends_request", "It sends a request using HTTP or HTTPS"),
    ("http_is", "HTTP is a protocol used to transfer web resources"),
    ("https_is", "HTTPS uses secure communication to protect data"),
    ("server_returns", "The web server receives the request and"),
    ("what_comes_back", "These may include HTML code, images, style information"),
    ("renders", "The browser interprets the HTML, retrieves any linked"),
    ("recap_1", "So the process is the user"),
    ("recap_2", "The browser extracts the domain name"),
    ("recap_3", "DNS finds the server's IP address"),
    ("recap_4", "The browser connects to the web server"),
    ("recap_5", "The server returns the requested resources"),
    ("recap_6", "The browser interprets those resources and displays the page"),
    ("distinction", "Keep one important"),
    ("dns_does", "DNS resolves the domain name to an IP address"),
    ("server_does", "The web server returns the web page resources"),

    # --------------------------------------------------------- 5. cookies
    ("cookies_open", "Websites often need to remember information about a user"),
    ("cookie_is", "A cookie is a small piece of data stored by the browser"),
    ("cookies_convenient", "Cookies can make a website more convenient"),
    ("basket", "they may help a shopping website remember the items"),
    ("preferences", "They can also remember preferences or help maintain"),
    ("two_types", "There are two cookie types you need to distinguish"),
    ("named", "Session cookies and persistent cookies"),
    ("session_is", "A session cookie normally remains only while the current"),
    ("session_deleted", "It may be deleted when the user closes the browser"),
    ("session_use", "A website might use one to remember items in a shopping"),
    ("persistent_is", "A persistent cookie remains after the browser is closed"),
    ("persistent_until", "It is stored until it expires or"),
    ("persistent_use", "A website might use one to remember a preference"),
    ("privacy", "Cookies can improve convenience, but they also raise privacy"),
    ("tracking", "persistent cookies can be used to track a user's behavior"),
    ("compare_cookies", "compare how long each one lasts"),

    # ------------------------------------------ 6. digital currency, blockchain
    ("currency_open", "The internet also supports"),
    ("currency_is", "Digital currency exists electronically and can be transferred"),
    ("uses_blockchain", "Some digital currencies use a blockchain to record"),
    ("ledger", "A blockchain is a digital ledger made up of linked records"),
    ("simplified", "Here is a simplified explanation"),
    ("broadcast", "A transaction is requested and broadcast to computers"),
    ("network_checks", "The network checks whether the transaction"),
    ("grouped", "Valid transactions are grouped into a"),
    ("timestamp_link", "The block includes a timestamp and a cryptographic link"),
    ("replicated", "When the network accepts the block, it is added"),
    ("changing_older", "changing an older record would affect the links"),
    ("needs_network", "An attacker would also need the"),
    ("difficult", "This makes undetected changes difficult"),
    ("not_impossible", "do not say that every blockchain chain is completely"),
    ("accurate", "The accurate explanation is that the linked records"),

    # -------------------------------------------------------- 7. the threats
    ("threats_open", "Now let's turn to cybersecurity threats"),
    ("threat_is", "A cybersecurity threat is an action or piece of software"),
    ("different_ways", "Different threats work in different ways"),
    ("brute_force", "A brute force attack tries many possible password"),
    ("interception", "Data interception happens when someone captures data"),
    ("hacking", "Hacking means gaining unauthorized access"),
    ("ddos", "a distributed denial of service attack, or DDoS attack"),
    ("ddos_flood", "uses many devices to flood"),
    ("ddos_aim", "The aim is to make that service slow or unavailable"),
    ("availability", "It targets availability"),

    # ------------------------------------------------------------ 8. malware
    ("malware_open", "Malware is malicious software"),
    ("malware_types", "There are several different types of malware"),
    ("virus", "A virus attaches itself to a file or program"),
    ("worm", "A worm can copy itself and spread across networks"),
    ("trojan", "A Trojan horse appears legitimate or useful"),
    ("spyware", "Spyware secretly records activity"),
    ("adware", "Adware displays unwanted advertising"),
    ("ransomware", "Ransomware encrypts or locks data and demands payment"),
    ("mechanisms", "These terms describe different mechanisms"),
    ("virus_host", "A virus needs a host file"),
    ("worm_self", "A worm can self"),
    ("trojan_deceives", "A Trojan horse deceives the user"),
    ("ransomware_blocks", "Ransomware prevents access to data"),
    ("spyware_collects", "Spyware secretly collects information"),
    ("too_vague", "Calling all of these threats a virus is too vague"),
    ("name_it", "Name this specific threat and explain how it works"),

    # --------------------------------------- 9. deceiving people, not machines
    ("deceive_open", "Some attacks focus on deceiving people"),
    ("phishing_is", "Fishing uses a fraudulent message to trick someone"),
    ("phishing_bank", "a message might pretend to come from a bank"),
    ("phishing_link", "The message may include a link to a fake website"),
    ("pharming_is", "Farming is different"),
    ("pharming_how", "It redirects the user to a fake website"),
    ("pharming_cause", "The redirection may be caused by malicious code"),
    ("keep_clear", "Keep the distinction clear"),
    ("phishing_short", "Fishing users a deceptive message to persuade"),
    ("pharming_short", "Farming redirects the"),
    ("social_is", "Social engineering is the broader practice of manipulating"),
    ("pretend", "An attacker may pretend to be a colleague, a technician"),
    ("social_aim", "The attacker's aim might be to persuade someone to reveal"),
    ("not_only_software", "Security is not only about software and devices"),
    ("people_decide", "people's decisions also affect security"),

    # -------------------------------------------------------- 10. the controls
    ("controls_open", "Let's match security controls to the threats"),
    ("authentication", "Authentication checks that a user is who they claim"),
    ("auth_kinds", "It may use a password, a biometric check"),
    ("two_step", "verification requires an additional check after the password"),
    ("code_to_device", "a user may need to enter a code sent to a separate"),
    ("stolen_password", "This can reduce the risk of someone accessing an account"),
    ("access_levels", "Access levels limit which resources each user can use"),
    ("student_account", "a student account may be allowed to view a file"),
    ("firewall", "A firewall filters network traffic according to a set"),
    ("firewall_limits", "although it cannot prevent every type"),
    ("antimalware", "software can detect, quarantine, and remove"),
    ("updates", "Automatic updates install fixes for known vulnerabilities"),
    ("updates_why", "keeping software updated can reduce the chance"),
    ("encryption", "protects data as it travels between devices"),
    ("https_again", "HTTPS uses secure communication based on encryption"),
    ("certificate", "A valid security certificate can help the browser verify"),
    ("https_limit", "But HTTPS does not prove that every"),
    ("fake_still_lies", "A fake website can still make false claims"),
    ("proxy", "A proxy server acts as an intermediary"),
    ("proxy_does", "It can filter requests or help hide the internal addresses"),
    ("privacy_settings", "Privacy settings can limit the personal information"),
    ("check_message", "Users can also check the sender, wording"),
    ("check_link", "Before entering bank details, they should check whether"),
    ("no_single", "No single security control stops every threat"),
    ("layers", "security is strongest when several controls work together"),

    # ------------------------------------------------- 11. one example
    ("example_open", "Let's apply these ideas to a message asking"),
    ("check_sender", "First, check who sent it"),
    ("sender_address", "Look carefully at the sender's address"),
    ("check_wording", "Next, check the wording"),
    ("wording_signs", "Poor spelling, a threatening tone or an urgent demand"),
    ("check_destination", "Then inspect the destination of any link"),
    ("text_vs_address", "The visible text may not match the actual website"),
    ("do_not_enter", "do not enter private details through an unexpected link"),
    ("contact_directly", "contact the bank using a trusted phone number"),
    ("two_step_helps", "verification can provide extra protection if a password"),
    ("but_not_the_code", "it cannot make it safe to give"),
    ("both_matter", "Technical controls matter and careful user behavior"),

    # ----------------------------------------------------------- 12. recap
    ("recap_open", "Let's finish with the main ideas"),
    ("r_internet", "The Internet is the network infrastructure"),
    ("r_web", "The World Wide Web is a collection of web pages"),
    ("r_dns", "DNS resolves the domain name to an IP address"),
    ("r_browser", "The browser connects to the web server, requests resources"),
    ("r_cookies", "persistent cookies differ mainly in how long they remain"),
    ("r_blockchain", "A blockchain is a linked timestamp digital ledger"),
    ("r_threats", "Cybersecurity threats use different methods"),
    ("r_virus", "A virus attaches to a host file"),
    ("r_worm", "A worm can self"),
    ("r_phishing", "Fishing uses deceptive messages, while farming redirects"),
    ("r_ddos", "A DDOS attack aims to make a service unavailable"),
    ("r_ransomware", "Ransomware locks or encrypts data and demands payment"),
    ("r_layers", "Security works best in layers"),
    ("r_controls", "authentication, access levels, firewalls"),
    ("r_each", "each help reduce different risks"),
    ("exam_advice", "identify the threat or technology precisely"),
    ("connect_control", "connect the security control to the risk"),
    ("close", "That is the key to writing clear"),
]

if __name__ == "__main__":
    build("CH05-internet", "cs.internet", BEATS, "CH05-internet",
          "Cambridge O Level 2210 Chapter 5: The Internet and Its Uses. "
          "Anchors copied from the transcript, mis-hearings and all.")
