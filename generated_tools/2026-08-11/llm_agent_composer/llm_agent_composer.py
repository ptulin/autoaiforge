import argparse
import json
from transformers import AutoModelForSequenceClassification
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression


def compose_agents(agent_models, composition_config):
    estimators = []
    for model in agent_models:
        estimator = (model, AutoModelForSequenceClassification.from_pretrained(model))
        estimators.append(estimator)
    if not agent_models:
        return None
    if 'weights' not in composition_config:
        raise ValueError('Composition config must contain weights')
    if len(agent_models) != len(composition_config['weights']):
        raise ValueError('Number of agent models must match number of weights')
    voting_classifier = VotingClassifier(estimators=estimators, voting='soft', weights=composition_config['weights'])
    return voting_classifier

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LLM Agent Composer')
    parser.add_argument('--agents', nargs='+', help='List of LLM agent models')
    parser.add_argument('--composition_config', help='Composition config file')
    args = parser.parse_args()
    with open(args.composition_config, 'r') as f:
        composition_config = json.load(f)
    composed_agent = compose_agents(args.agents, composition_config)
    print(composed_agent)