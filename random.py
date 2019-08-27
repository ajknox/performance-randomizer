import random
from improvers import improvers # just a list of improvers
# seed = 1234567890
# random.seed(seed)

# how many people are in each show
show_sizes = [8, 8]
# total_slots = reduce(lambda x, y: x + y, show_sizes)
total_slots = sum(show_sizes)
double_slots = total_slots - len(improvers)
single_show_sizes = [show_size - double_slots for show_size in show_sizes]

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





# random.shuffle(improvers)
# go_twice = []
# for i in [1,2,3]:
#     go_twice.append(improvers.pop())
# print(go_twice)
#
#
# import random
# seed = 91823712309487123 + 17
# people = [
#     'Alice',
#     'Bob',
#     'Carol',
#     'Eve',
#     ]
# people.sort()
# random.seed(seed)
#
# print(people)
