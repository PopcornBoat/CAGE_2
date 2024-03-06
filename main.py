from CybORG import CybORG
from CybORG.Agents.Wrappers import ChallengeWrapper
import inspect
from CybORG.Agents import B_lineAgent, GreenAgent, BlueMonitorAgent
from pprint import pprint
path = str(inspect.getfile(CybORG))
path = path[:-10] + '/Shared/Scenarios/Scenario2.yaml'

agents = {
    #'Red': B_lineAgent,
    #'Green': GreenAgent
}
agent = BlueMonitorAgent()

env = CybORG(path,'sim',agents=agents)
env = ChallengeWrapper(env=env,agent_name='Blue')

obs = env.reset()
action_space = env.action_space

actions = [51, 55, 116, 133, 134, 135, 139, 3, 4, 5, 9, 16, 17, 18, 22, 11, 12, 13, 14, 141, 142, 143, 144, 132, 2, 15, 24, 25, 26, 27]

for i in range(len(actions)):
    # action = agent.get_action(obs,action_space=action_space)
    # print('action')
    # print(action)
    step = actions[i]
    print(80*"=")
    print("action: ", step)

    obs, reward, done, info = env.step(step)
    pprint(env.get_observation("Blue"))
    # print(obs)
    print(76 * '-')
    print(reward)
    # print(76 * '-')
    # print(done)
    print(76 * '-')
    pprint(info)
    print(80 * "=")
# action = 2
#
# obs, reward, done, info = env.step(action)





