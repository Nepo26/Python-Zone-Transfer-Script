#!/bin/python3

import dns.query
import dns.resolver
import dns.zone
import sys

if len(sys.argv) > 1:
    try:
        if sys.argv[2] == "-s":
            silent=True
    except IndexError:
        silent=False
else:
    print(
"""DNS Zone Transfer Test Script v0.0.1"
Usage: {sys.argv[0]} [Options]  {target domain}
OPTIONS:
    -s: silent, just prints info if could transfer domain
""" )
    sys.exit()


print("DNS Zone Transfer Test Script v0.0.1" )

domain=sys.argv[1]

print("Resolving DNS...")
soa_answer = dns.resolver.resolve(domain, 'SOA')

for ns in soa_answer.response.authority[0]:
    master_answer = dns.resolver.resolve(ns.target,'A')
    try:
        zone=dns.zone.from_xfr(dns.query.xfr(master_answer[0].address, domain))
    except:
        continue
    if not silent:
        print(f"Zone file of {ns.target}:")
    for n in sorted(zone.nodes.keys()):
        print(zone[n].to_text(n))

#master_answer = dns.resolver.resolve(soa_answer[0].mname, 'A')
#dns.zone.from_xfr(dns.query.xfr(master_answer[0].address, 'dnspython.org'))
#for n in sorted(z.nodes.keys()):
#        print(z[n].to_text(n))




#temp=vars(soa_answer)
#for item in temp:
#        print(item, ':', temp[item])
