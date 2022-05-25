
# NOTE:
# Warning! This is early stage, experimental, 'pre-alpha' code.
# This is a demo. Toy AIs are used. Data and the implementation
# is for demo purposes only and require further checks and work.
# (For example, current 'prevalence' values that are used are
# not necessarily the correct prevalence.)
#
# (The text below is based on text from the MIT licence.)
# THE SOFTWARE/DATA ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
# (OR ANYTHING SIMILAR),
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE/DATA OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE/DATA.



# Toy AIs.

import json
import random


random.seed(1)


def toy_AI_one(case):
    THRESHOLD = 0.25

    val = None
    if random.random() < THRESHOLD:
        val = True
    else:
        val = False
    return val


def toy_AI_two(case):
    THRESHOLD = 0.75

    val = None
    if random.random() < THRESHOLD:
        val = True
    else:
        val = False
    return val
    
    
AIs = {
    "Toy AI one (random predictions with prob. = 25%)": toy_AI_one,
    "Toy AI two (random predictions with prob. = 75%)": toy_AI_two,
}


cases = json.load(open("output/synthetic_cases_test.json"))

output = []
for case in cases:
    vals = {}
    for AI_name, AI_func in AIs.items():
        vals[AI_name] = AI_func(case)
    output.append(vals)

json.dump(
    {
        'AIs': list(AIs.keys()),
        'outputs': output,
    },
    open("output/AIs_output.json", "w"),
    indent=2,
)
