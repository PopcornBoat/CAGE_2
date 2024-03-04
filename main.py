# test Red actions
import inspect
import random
from pprint import pprint
from CybORG import CybORG
from CybORG.Agents import *
from CybORG.Shared.Actions import *
from CybORG.Agents.Wrappers import *
from Agents.BlueGreedyDecoy import *
from New_Wrappers.NewTrueTableWrapper import NewTrueTableWrapper

path = str(inspect.getfile(CybORG))
path = path[:-10] + '/Shared/Scenarios/Scenario2.yaml'

# env = CybORG(path, 'sim', agents={'Red': B_lineAgent})
# # env = BlueTableWrapper(env=cyborg, output_mode='table')
#
# agent = BlueMonitorAgent()
#
# results = env.reset('Blue')
# obs = results.observation
# action_space = results.action_space
# action = DecoyApache(session=0, agent='Blue', hostname='User1')
# results = env.step(action=action, agent='Blue')
# pprint(results.observation)
# # pprint(env.get_agent_state('Blue')['User2'])
# for i in range(20):
#     pprint(obs)
#     action = agent.get_action(obs,action_space)
#     results = env.step(action=action, agent='Blue')
#     obs = results.observation
#     blue_obs = env.get_agent_state('True')
#     # list all sessions
#     print(50*"+")
#     pprint(blue_obs['User1']['Sessions'])
#     print(50*"+")
#

'''
Try to construct some actions to test Decoys
'''
# env = CybORG(path, 'sim')
# results = env.reset('Blue')
# print(50 * "+")
# pprint(results.action_space)
# print(50 * "+")
# user1_IP = results.observation['User1']['Interface'][0]['IP Address']
# user1_subnet = results.observation['User1']['Interface'][0]['Subnet']
# pprint(results.observation['User1']['Sessions'])
#
# # red discover subnet first
# action = DiscoverRemoteSystems(subnet=user1_subnet, session=0, agent='Red')
# results = env.step(action=action, agent='Red')
#
# # red discover services on user1 - before decoy
# action = DiscoverNetworkServices(ip_address=user1_IP, session=0, agent='Red')
# results = env.step(action=action, agent='Red')
# print('red obs before decoy')
# pprint(results.observation)
# print(76 * "=")
# print('blue obs before decoy')
# blue_obs = env.get_observation('Blue')
# pprint(blue_obs['User1'])
# print('TRUE STATE')
# pprint(env.get_agent_state('True')['User1'])
# print(">>>>>>>>>>>>>>>>>>>>>")
# # blue setup decoy on user1
# action = DecoyApache(session=0, agent='Blue', hostname='User1')
# results = env.step(action=action, agent='Blue')
# print('TRUE STATE')
# pprint(env.get_agent_state('True')['User1'])
# print(">>>>>>>>>>>>>>>>>>>>>")
#
# print("Decoy info")
# pprint(results.observation)
#
# # red discover services on user1
# action = DiscoverNetworkServices(ip_address=user1_IP, session=0, agent='Red')
# results = env.step(action=action, agent='Red')
# print('red obs after decoy')
# pprint(env.get_observation('Red'))
# print(76 * "=")
# print('blue obs after decoy')
# blue_obs = env.get_observation('Blue')
# pprint(blue_obs)

'''
    Decoy agent tests
'''

agents = {
    'Red': B_lineAgent,
    'Green': GreenAgent
}

env = CybORG(path, 'sim', agents=agents)

results = env.reset(agent='Blue')
obs = results.observation
action_space = results.action_space
agent = BlueGreedyDecoy()

total_reward = []
r = []
for step in range(100):
    print("Step: ", step)


    action = agent.get_action(obs, action_space=action_space)
    results = env.step(agent='Blue', action=action)
    obs = results.observation
    reward = results.reward
    done = results.done
    info = results.info

    # print("Done: ", done)
    # print("Info: ", info)
    r.append(reward)
    total_reward.append(round(sum(r), 2))
    print(reward)

    # if done: break

print(20 * "+", " Final Reward: ", total_reward[-1], 20 * "=")
print(total_reward)
