A picker to help us fairly choose which people will perform in which improv show.

There are usually two separate shows that may have different forms. A variable number of people may perform in each show.

Each eligible person gets to vote on a few things:
- if they want to go in both shows if available
- which forms they want to participate in
- which forms they will strictly prefer if available

Example of a person expressing preference:
{
  'Alice': {
    'go_twice': True,
    'try_unknown_form': False,
    'Harold': 1,
    'Scones': 1,
    'Monoscene': False,
    'Montage': 2,
    'Statue Park': 3,
  }
}

Here, Alice is expressing that she is willing to go twice, has equal preference for Harold and Scones, lower preference for Montage and lower still for Statue Park, and would refuse to perform in a Monoscene or any form she hasn't explicitly listed.

Axioms
- Everyone must perform at least once.
- No one should be placed into a lower priority form if a higher priority one was available and not full.
- No one should be able to increase their chance of going twice by carefully choosing their ballot.
- The two forms selected should be chosen so that the maximum number of people get their highest priority form.
- Each person may rank any number of forms, with natural number priority scores, lower is higher priority.
- Multiple forms may have the same rank form the same person
- Each person can only express one preference for a specific form

Method:
- determine how many people will need to go twice
- take every form that got at least 1 first or second place vote and at least 4 votes overall
- for each combination of those forms (scenario)
  - find participants that said they would only participate in one of the forms and assign them to that form
  - find participants that expressed no preference between the two forms and reserve them, including participants that said they would not perform in either form
  - randomly order other participants
  - assign each participant to their preferred form until the form is full, filling the other form if necessary
  - randomly assign participants that expressed no preference until all slots full
- maybe a future version can choose a condorcet winner of scenarios using the smith-minimax method
- for now, we'll vote out the least popular scenarios in a runoff
  - each participant votes for the scenario that _least_ reflects their preferences, randomly voting if a tie. Hierarchy of voting rules
    - a participant always votes for scenarios which do not include a form they want to perform in
    - a participant who wants to perform in in two sets will vote for a scenario which includes a form they don't want to perform in
    - vote for the scenario which places the participant in the worst priority form
    - if all scenarios have the participant in equal priority forms, do not vote
  - if all scenarios equally reflect their preferences, they do not vote
  - the scenario with the most votes is eliminated, randomly select one if there is a tie
  - if there were no votes this round, randomly eliminate all buy one scenario
  - repeat until there is only one scenario left
- randomly select people to go twice from all participants that want to go twice, and the form they are not in is not a form they said they would not perform in
