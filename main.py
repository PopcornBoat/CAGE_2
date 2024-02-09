# test Red actions
import inspect
import random
from pprint import pprint
from CybORG import CybORG
from CybORG.Agents import *
from CybORG.Shared.Actions import *
from CybORG.Agents.Wrappers import BlueTableWrapper, RedTableWrapper

path = str(inspect.getfile(CybORG))
path = path[:-10] + '/Shared/Scenarios/Scenario2.yaml'

cyborg = CybORG(path, 'sim')
env = RedTableWrapper(env=cyborg, output_mode='table')

agent = KeyboardAgent()

results = env.reset('Red')
obs = results.observation
action_space = results.action_space

for i in range(100):
    print(obs)
    action = agent.get_action(obs,action_space)
    results = env.step(action=action,agent='Red')
    obs = results.observation
    blue_obs = env.get_observation('Blue')
    print("========== Blue OBS ======")
    pprint(blue_obs)
    print("Blue OBS end")


'''
Try to construct some actions to test Decoys
'''
# env = CybORG(path, 'sim')
# results = env.reset('Blue')
# user1_IP = results.observation['User1']['Interface'][0]['IP Address']
# user1_subnet = results.observation['User1']['Interface'][0]['Subnet']
# pprint(results.observation['User1']['Sessions'][0])
#
# # red discover subnet first
# action = DiscoverRemoteSystems(subnet=user1_subnet, session=0, agent='Red')
# results = env.step(action=action, agent='Red')
#
#
# # red discover services on user1 - before decoy
# action = DiscoverNetworkServices(ip_address=user1_IP, session=0, agent='Red')
# results = env.step(action=action, agent='Red')
# print('red obs before decoy')
# pprint(results.observation)
# print(76*"=")
# print('blue obs before decoy')
# blue_obs = env.get_observation('Blue')
# pprint(blue_obs['User1'])
#
# # blue setup decoy on user1
# action = DecoyApache(session=0, agent='Blue', hostname='User1')
# results = env.step(action=action, agent='Blue')
# print("Decoy info")
# pprint(results.observation)
#
# # red discover services on user1
# action = DiscoverNetworkServices(ip_address=user1_IP, session=2, agent='Red')
# results = env.step(action=action, agent='Red')
# print('red obs after decoy')
# pprint(results.observation)
# print(76*"=")
# print('blue obs after decoy')
# blue_obs = env.get_observation('Blue')
# pprint(blue_obs)