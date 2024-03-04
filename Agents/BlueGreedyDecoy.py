from CybORG.Agents.SimpleAgents.BaseAgent import BaseAgent
from CybORG.Shared import Results
from CybORG.Shared.Actions import (Monitor, Remove, DecoyApache, DecoySSHD, DecoyTomcat, DecoyVsftpd, DecoySvchost,
                                   DecoySmss,
                                   DecoyFemitter, DecoyHarakaSMPT)
from pprint import pprint

from CybORG.Shared.Enums import OperatingSystemType
import random


class BlueGreedyDecoy(BaseAgent):
    def __init__(self):
        self.host_list = []
        self.last_action = None
        self.init_run = True
        self.host_os_dict = {}

    def train(self, results: Results):
        pass

    def get_action(self, observation, action_space):
        # add suspicious hosts to the hostlist if monitor found something
        # added line to allow for automatic monitoring.
        if self.last_action is not None and self.last_action == 'Monitor':
            for host_name, host_info in [(value['System info']['Hostname'], value) for key, value in observation.items()
                                         if key != 'success']:
                if host_name not in self.host_list and host_name != 'User0' and 'Processes' in host_info and len(
                        [i for i in host_info['Processes'] if 'PID' in i]) > 0:
                    self.host_list.append(host_name)

        # assume a single session in the action space
        #session = list(action_space['session'].keys())[0]
        # test output
        # print("session: ")
        # pprint(session)
        # print("Action space")
        # pprint(action_space['port'])
        # pprint(action_space)
        # pprint(action_space['agent'])
        print(76 * "=")
        # pprint(observation.keys())

        # get host and os pairs
        if self.init_run:
            self.host_os_dict = self._extract_hostname_ostype(observation)

        if not self.host_os_dict: print("Hostname : OSType pair not available!")

        # Monitor / Decoy
        if len(self.host_list) == 0:
            self.last_action = 'Active Decoy'
            print('Decoy')
            random_key = self.generate_key()
            print(random_key)

            return self.create_decoy(hostname=random_key)
        else:
            self.last_action = 'Passive Decoy'
            print('Decoy')
            random_key = self.generate_key()
            print(random_key)

            self.host_list.pop(0)
            return self.create_decoy(hostname=random_key)

    def end_episode(self):
        self.host_list = []
        self.last_action = None

    def set_initial_values(self, action_space, observation):
        pass

    def _extract_hostname_ostype(self, observation: dict) -> dict:
        host_os_pair = {}
        #pprint(observation)
        # Create an iterator from the dictionary and skip the first item
        iter_data = iter(observation.items())
        next(iter_data, None)  # Skip the first item

        # Iterate over the remaining items
        for key, value in iter_data:
            # Extracting hostname
            hostname = value.get('System info', {}).get('Hostname', 'Unknown')

            # Extracting OSType
            os_type = value.get('System info', {}).get('OSType', 'Unknown')

            host_os_pair[hostname] = os_type

        self.init_run = False
        return host_os_pair

    def create_decoy(self, hostname: str, session: int = 0, agent: str = 'Blue'):
        """
        :param hostname:
        :param session:
        :param agent:
        :return: action
        """
        # get open ports and OS on the host
        os_type = self.host_os_dict[hostname]
        # Categorize decoys based on OS requirement
        os_independent = [DecoyApache, DecoySSHD, DecoyTomcat]
        linux_required = [DecoyHarakaSMPT, DecoyVsftpd]
        windows_required = [DecoyFemitter, DecoySmss, DecoySvchost]

        # Filter decoys based on OS type
        if os_type == 'OperatingSystemType.LINUX':
            eligible_decoys = linux_required + os_independent
        elif os_type == 'OperatingSystemType.WINDOWS':
            eligible_decoys = windows_required + os_independent
        else:
            # If OS type is unknown or not specified, consider all decoys
            eligible_decoys = linux_required + windows_required + os_independent

        # Randomly select a decoy
        selected_decoy_class = random.choice(eligible_decoys)

        # Create an instance of the selected decoy
        decoy_instance = selected_decoy_class(session=0, agent='Blue', hostname=hostname)
        print("Selected Decoy: ", decoy_instance)
        return decoy_instance



    def generate_key(self) -> str:
        # Exclude certain keys
        excluded_keys = ['Defender', 'User0', 'Op_Host0', 'Op_Host1', 'Op_Host2']

        # Create a list of keys excluding the ones in excluded_keys
        filtered_keys = [key for key in self.host_os_dict.keys() if key not in excluded_keys]

        # Randomly select a key from the filtered list
        random_key = random.choice(filtered_keys)

        return random_key
