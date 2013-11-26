#!/usr/bin/python
""" Query Google Safe Browsing-API for given domain(s)

More info: https://developers.google.com/safe-browsing/
"""

try:
    import sys, urllib, urllib2
except ImportError:
    print "ImportError: Required modules could not be found."
    sys.exit(1)

api_url = "https://sb-ssl.google.com/safebrowsing/api/lookup"

params = {
    'client': 'nagios',
    'apikey': '<insert api key here>',
    'appver': '1.0',
    'pver': '3.0'
}

# 0 = OK or UP
# 1 = WARNING UP or DOWN/UNREACHABLE
# 2 = CRITICAL or DOWN/UNREACHABLE
# 3 = UNKNOWN or DOWN/UNREACHABLE


def fetch_data(req):
    try:
        return urllib2.urlopen(req)
    except urllib2.URLError as e:
        sys.stderr.write("Error: %s" % (e.reason,))
        return 1


def missing_args(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s domain(s)\n" % (argv[0],))
        return 1
    else:
        # print argv
        return


def build_request(argv):
    url = api_url + '?' + urllib.urlencode(params)
    data = str(len(argv[1:])) + "\n" + "\n".join(argv[1:])
    return urllib2.Request(url, data)


def main(argv):

    if not missing_args(argv):
        req = build_request(argv)
        response = fetch_data(req)

        try:
            if response.getcode() == 200:
                # One or more domains not Ok
                body = response.read()
                status = body.split("\n")
                
                # Iterate domains and print affected
                for i in range(len(argv[1:])):
                    # print (i+1), argv[(i+1)], status[i]
                    if status[i] != "ok":
                        print argv[(i+1)]
                return 2
                
            elif response.getcode() == 204:
                # All domains ok
                print "Ok"
                return
            else:
                return 3
        except Exception:
            # print "An error occurred."
            return 3

if __name__ == '__main__':
    sys.exit(main(sys.argv))