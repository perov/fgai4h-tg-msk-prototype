
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


import json
import copy
import numpy
import tqdm

NUM_SAMPLES = 1_000

rng = numpy.random.default_rng(1)

cases = json.load(open("output/original_cases.json"))

synthetic_cases = []
synthetic_cases_test = []

for synthetic_case_id in tqdm.tqdm(range(NUM_SAMPLES)):
    while True:
        random_case_id = rng.integers(len(cases) - 1)
        synthetic_case = copy.deepcopy(cases[random_case_id])
        synthetic_case['Age'] = (
            round(float(synthetic_case['Age'])) + int(rng.integers(-5, 5 + 1))
        )
        if synthetic_case['Age'] < 18:
            continue
            
        chance_of_recovery_improvement = synthetic_case['% chance of recovery/improvement']
        
        if "%" not in chance_of_recovery_improvement:
            continue
        
        chance_of_recovery_improvement = chance_of_recovery_improvement.strip()
        chance_of_recovery_improvement = chance_of_recovery_improvement.replace("%%", "")
        chance_of_recovery_improvement = chance_of_recovery_improvement.replace("%", "")
        try:
            chance_of_recovery_improvement = float(chance_of_recovery_improvement) / 100
        except ValueError:
            try:
                chance_of_recovery_improvement = chance_of_recovery_improvement.split("-")
                chance_of_recovery_improvement = (
                    (
                        float(chance_of_recovery_improvement[0]) +
                        float(chance_of_recovery_improvement[1])
                    ) / 2 / 100
                )
            except IndexError:
                continue
            except ValueError:
                continue
                
        assert chance_of_recovery_improvement >= 0 and chance_of_recovery_improvement <= 1
            
        synthetic_case['disability_weight'] = float(
            synthetic_case['Average disability weight'].strip().split(" ")[0]
        )
            
        if rng.random() < chance_of_recovery_improvement:
            synthetic_case['Recovery / Improvement (Sampled)'] = True
        else:
            synthetic_case['Recovery / Improvement (Sampled)'] = False
            
        synthetic_case['prevalence'] = synthetic_case['Prevalence Number Demo (not necessarily correct; to be checked!)']
        if "%" in synthetic_case['prevalence']:
            synthetic_case['prevalence'] = float(synthetic_case['prevalence'].replace("%", "")) / 100
        else:
            synthetic_case['prevalence'] = None
    
        break
        
    synthetic_cases.append(synthetic_case)
    
    synthetic_case_test = {}
    for key in [
        "Age",
        "Gender",
        "Ethnicity",
        "Symptoms (Pain)",
        "Pain irritability",
        # TODO: to add other fields
    ]:
        synthetic_case_test[key] = synthetic_case[key]
    synthetic_cases_test.append(synthetic_case_test)

json.dump(
    synthetic_cases,
    open("output/synthetic_cases.json", "w"),
    indent=2,
)
json.dump(
    synthetic_cases_test,
    open("output/synthetic_cases_test.json", "w"),
    indent=2,
)
