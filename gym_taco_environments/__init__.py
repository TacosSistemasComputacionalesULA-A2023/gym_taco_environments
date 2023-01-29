from gym.envs.registration import register

register(
    id='TwoArmedBandit-v0',
    entry_point='gym_taco_environments.envs:TwoArmedBanditEnvV0',
)

register(
    id='FrozenLake-v0',
    entry_point='gym_taco_environments.envs:FrozenLakeEnvV0',
)