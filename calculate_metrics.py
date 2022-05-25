
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


from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
import json
from datetime import datetime
from datetime import timezone
import html

cases = json.load(open("output/synthetic_cases.json"))
outputs = json.load(open("output/AIs_output.json"))

y_true = []

for index, case in enumerate(cases):
    y_true.append(case["Recovery / Improvement (Sampled)"])

metrics = (
    ('Accuracy', accuracy_score),
    ('F1', f1_score),
    ('Precision', precision_score),
    ('Recall', recall_score),
    ('ROC AUC', roc_auc_score),
)

html_output = "<html><body><h1>Topic Group MSK Medicine, part of the ITU/WHO Focus Group on Artificial Intelligence for Health</h1>"
html_output += "<hr><b><font color='red'>Warning! This is early stage, experimental, 'pre-alpha' code. This is a demo. Toy AIs are used. Data and the implementation is for demo purposes only and require further checks and work. (For example, current 'prevalence' values that are used are not necessarily the correct prevalence.)</font></b><hr>"
html_output += "<i>Generated: " + html.escape(datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S %Z")) + "</i>"

html_output += "<hr><b>Number of cases: " + str(len(y_true)) + "</b>"

for AI_name in outputs['AIs']:
    output = [
        el[AI_name]
        for el in outputs['outputs']
    ]

    html_output += "<hr><br><hr><h2>" + AI_name + "</h2>"

    def str_metric_value(val):
        val = str(round(val * 100, 2)) + "%"
        return val

    html_output += "<hr><h3>Unweighted</h3>"

    for metric in metrics:
        html_output += "<b>" + html.escape(metric[0]) + "</b>: " + str_metric_value(metric[1](
            y_true,
            output,
        )) + "<br>"

    html_output += "<hr><h3>Weighted by disability_weight</h3>"

    for metric in metrics:
        html_output += "<b>" + html.escape(metric[0]) + "</b>: " + str_metric_value(metric[1](
            y_true,
            output,
            sample_weight=[el['disability_weight'] for el in cases],
        )) + "<br>"

    html_output += "<hr><h3>Weighted by 'prevalence' (region X)</h3>"

    for metric in metrics:
        html_output += "<b>" + html.escape(metric[0]) + "</b>: " + str_metric_value(metric[1](
            y_true,
            output,
            sample_weight=[(lambda x: x if x is not None else 0.0)(el['prevalence']) for el in cases],
        )) + "<br>"
        
    html_output += "<br><br><br></body></html>"

with open("output/output.html", "w") as output_file:
    output_file.write(html_output)
