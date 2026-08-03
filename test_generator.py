


from agent_evals.generator import SyntheticGenerator


generator = SyntheticGenerator()

cases = generator.generate(topic="travel agent flight search queries", count=3)

for case in cases:
    print(case)
