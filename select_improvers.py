import random
from improvers import improvers # just a list of improvers
seed = 1234567890
random.seed(seed)

# how many people are in each show
show_sizes = [8, 8]
# total_slots = reduce(lambda x, y: x + y, show_sizes)
total_slots = sum(show_sizes)
double_slots = total_slots - len(improvers)
single_show_sizes = [show_size - double_slots for show_size in show_sizes]
single_show_size = single_show_sizes[0]

potential_forms = {}

for person, selection in improvers.items():
    for form, rank in selection.items():
        if rank in [1, 2] and form not in ['twice', 'other']:
            potential_forms[form] = 0
print('Forms with a first or second place vote: {forms}'.format(forms=', '.join([form for form in potential_forms])))

for form in potential_forms:
    for person, selection in improvers.items():
        if selection.get(form, False) > 0:
            potential_forms[form] += 1
print(f'People choosing each form: {potential_forms}')

forms = [form for form, votes in potential_forms.items() if votes >= 4]
print(f'Forms with at least 4 votes: {forms}')

n_forms = len(forms)
scenarios = []
for i in range(n_forms):
    for j in range(n_forms - i - 1):
        scenarios.append([forms[i], forms[i+j+1]])

print(f'Scenarios: {scenarios}')

def determine_preference(options):
    # return None if all the same
    if all(option == options[0] for option in options):
        return None
    return options.index(max(options))



def vote_scenario(name, choices, scenarios):
    # vote for scenarios with no preferred shows
    for i, scenario in enumerate(scenarios):
        if (
            (not choices.get(scenario[0], choices['other']))
            and (not choices.get(scenario[1], choices['other']))
        ):
            print(f'{name} voted for {scenario} because they disliked both forms')
            return i

    # vote if either is unpreferred and going twice
    if choices['twice']:
        for i, scenario in enumerate(scenarios):
            if (
                (not choices.get(scenario[0], choices['other']))
                or (not choices.get(scenario[1], choices['other']))
            ):
                print(f'{name} voted for {scenario} because they disliked one of the forms')
                return i
    # pick scenario with most preferred show
    options = [max([choices.get(scenario[0], 9999), choices.get(scenario[1], 9999)]) for scenario in scenarios]
    preference = determine_preference(options)
    if preference:
        return preference

    return 'no vote'



while(len(scenarios) > 1):
    # random.shuffle(scenarios)
    print('------------ Form Voting Round ------------')
    print(f'Scenarios still in consideration: {scenarios}')
    votes = [0 for _i in range(len(scenarios))]
    for name, choices in improvers.items():
        vote = vote_scenario(name, choices, scenarios)
        if vote != 'no vote':
            votes[vote] += 1
    print(f'Votes: {votes}')
    worst_scenario = determine_preference(votes)
    if worst_scenario:
        voted_off = scenarios.pop(worst_scenario)
    else:
        voted_off = scenarios.pop()
    print(f'{voted_off} was voted the worst scenario and removed.')

forms = scenarios[0]
print(f'========== Winning forms are {forms} ==========')

"""
- find participants that expressed no preference between the two forms and reserve them, including participants that said they would not perform in either form
- randomly order other participants
- assign each participant to their preferred form until the form is full, filling the other form if necessary
- randomly assign participants that expressed no preference until all slots full
- randomly select people to go twice from all participants that want to go twice, and the form they are not in is not a form they said they would not perform in
"""

set_lists = [[], []]
names = set([name for name in improvers])
for name, choices in improvers.items():
    if choices.get(forms[0], choices['other']) and not choices.get(forms[1], choices['other']):
        print(f"Assigned {name} to {forms[0]} because they don't want to perform in {forms[1]}")
        set_lists[0].append(name)
        names.remove(name)
    elif choices.get(forms[1], choices['other']) and not choices.get(forms[0], choices['other']):
        print(f"Assigned {name} to {forms[1]} because they don't want to perform in {forms[0]}")
        set_lists[1].append(name)
        names.remove(name)

# assign people with a preference:
full_sets = [False, False]
for name, choices in improvers.items():
    # skip people already assigned
    if name not in names:
        continue
    form_preferences = [choices.get(forms[i], choices['other']) for i in range(2)]
    for i in range(0):
        if len(set_lists[i]) >= single_show_size:
            print('{forms[i]} is full')
            full_sets[i] = True
    if form_preferences[0] < form_preferences[1] and not full_sets[0]:
        print(f"Assigned {name} to {forms[0]} because they prefer it")
        set_lists[0].append(name)
        names.remove(name)
    elif form_preferences[0] < form_preferences[1] and not full_sets[1]:
        print(f"Assigned {name} to {forms[1]} because they prefer it")
        set_lists[1].append(name)
        names.remove(name)

# assign everyone else
for name in names:
    for i in range(0):
        if len(set_lists[i]) >= single_show_size:
            print('{forms[i]} is full')
            full_sets[i] = True
    if full_sets[0]:
        random_selection = 1
    elif full_sets[1]:
        random_selection = 0
    else:
        random_selection = random.randrange(2)

    print(f"Assigned {name} to {forms[random_selection]} randomly.")
    set_lists[random_selection].append(name)

print(f'Set lists before going twice {set_lists}')

# lazy doubles assignement, not guaranteed to finish in finite time
for i, j in [[0,1], [1,0]]:
    while len(set_lists[i]) < show_sizes[i]:
        winner = random.choice(set_lists[j])
        print(f'Go twice winner: {winner}')
        if winner in set_lists[i]:
            print('    already in set')
        elif not improvers[winner].get(forms[i], choices['other']):
            print(f"    but they don't want to perform in {forms[i]}")
        else:
            print(f"    adding them to {forms[i]}")
            set_lists[i].append(winner)

print(f'Final set lists {forms} with {set_lists}')
