from gym.envs.registration import register

register(
    id="TwoArmedBandit-v0",
    entry_point="gym_taco_environments.envs:TwoArmedBanditEnvV0",
)

register(
    id="FrozenLake-v0",
    entry_point="gym_taco_environments.envs:FrozenLakeEnvV0",
)

register(
    id="FrozenMaze-v0",
    entry_point="gym_taco_environments.envs:FrozenMazeEnvV0",
)

register(
    id="RobotBattery-v0",
    entry_point="gym_taco_environments.envs:RobotBatteryEnvV0",
)

register(
    id="RobotMaze-v0",
    entry_point="gym_taco_environments.envs:RobotMazeEnvV0",
)

register(
    id="Princess-v0",
    entry_point="gym_taco_environments.envs:PrincessEnvV0",
)

register(
    id="BlockyRocks-v0",
    entry_point="gym_taco_environments.envs:BlockyRocksEnvV0",
)