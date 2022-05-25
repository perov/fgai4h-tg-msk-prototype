
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


import csv
import json
import os

fields = {}

case_id = -1

cases = []

# Data from https://docs.google.com/spreadsheets/d/1qIZYut9DzAkuTQYqA9aQJ4e5oxM8LnEZ7XPCvBm2DSs/edit#gid=0
# (tab 'Data')
with open('data/data.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row_id, row in enumerate(csvreader):
        if row_id == 1:
            for col_id, cell in enumerate(row):
                fields[col_id] = cell
        elif row_id >= 2 and row_id <= 20:
            case = {}
            for col_id, cell in enumerate(row):
                case[ fields[col_id] ] = cell
            cases.append(case)

os.makedirs("output", exist_ok=True)

json.dump(
    cases,
    open("output/original_cases.json", "w"),
    indent=2,
)
