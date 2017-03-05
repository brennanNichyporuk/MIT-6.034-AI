from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
	goalTree = OR(hypothesis)
	for rule in rules:
		for consequent in rule.consequent():
			bindings = match(consequent, hypothesis)
			if bindings != None:
				tp = AND() if isinstance(rule.antecedent(), AND) else OR()
				antecedents = rule.antecedent() 
				if not isinstance(antecedents, list): antecedents = [ antecedents ]
				for antecedent in antecedents:
					tp.append(backchain_to_goal_tree(rules, populate(antecedent, bindings)))
				print tp
				goalTree.append(tp)
	return simplify(goalTree)



# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
