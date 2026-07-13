import gymnasium as gym
from gymnasium import spaces
from environment.board_utils import Board
from environment.levels import GameLevels
from environment.actions import NUM_ACTIONS
from environment.observations import ObservationEncoder
import utils.config as config
from environment.actions import DIRECTIONS
from environment.deadlock import DeadlockDetector
from environment.renderer import Renderer

class SokobanEnv(gym.Env):

    def __init__(self, level_id=0):
        super().__init__()

        self.level_id = level_id
        self.renderer = Renderer()
        self.initialized_board = Board.pad_board(GameLevels.levels(level_id))
        self.board = Board.copy_grid(self.initialized_board)

        self.player_row, self.player_col = Board.find_player(self.board)

        self.steps = 0
        self.total_reward = 0

        #Gymnasium spaces
        self.action_space = spaces.Discrete(NUM_ACTIONS)

        height = len(self.board)
        width = len(self.board[0])

        self.observation_space = ObservationEncoder.observation_space(height, width)


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.board = Board.copy_grid(self.initialized_board)

        self.player_row, self.player_col = Board.find_player(self.board)

        self.steps = 0
        self.total_reward = 0

        observation = ObservationEncoder.encode(self.board)

        info = { "level": self.level_id, "steps": self.steps}

        return observation, info


    def step(self, action):

        self.steps += 1

        moved, pushed_box, box_on_target, invalid_move, box_left_target  = self._apply_action(action)

        deadlock = False
        completed = False
        terminated = False
        truncated = False

        #Check terminal conditions only if the move was valid
        if not invalid_move:

            deadlock = DeadlockDetector.isDeadlock(self.board)
            completed = Board.is_completed(self.board)

            if deadlock or completed:
                terminated = True

        #Episode reached maximum number of steps
        if self.steps >= config.MAX_STEPS:
            truncated = True

        reward = self._calculate_reward(
            moved=moved,
            pushed_box=pushed_box,
            box_on_target=box_on_target,
            invalid_move=invalid_move,
            deadlock=deadlock,
            completed=completed,
            box_left_target = box_left_target
        )

        #Extra penalty if episode stopped because of step limit
        if truncated:
            reward += config.STEP_LIMIT

        self.total_reward += reward

        observation = self._get_observation()
        info = self._get_info(completed=completed, deadlock=deadlock, invalid_move=invalid_move)

        return observation, reward, terminated, truncated, info

    def render(self):
        
        if self.renderer is not None:
            self.renderer.render(self.board)

    def close(self):
        
        if self.renderer is not None:
            self.renderer.close()

    def _get_observation(self):
        return ObservationEncoder.encode(self.board)

    
    def _calculate_reward(
        self,
        moved,
        pushed_box,
        box_on_target,
        invalid_move,
        deadlock,
        completed,
        box_left_target
    ):

        reward = 0.0

        if invalid_move:
            reward += config.INVALID_MOVE
            return reward
        if moved:
            reward += config.MOVE

        if pushed_box:
            reward += config.BOX_PUSH

        if box_on_target:
            reward += config.BOX_ON_TARGET

        if deadlock:
            reward += config.DEADLOCK

        if completed:
            reward += config.LEVEL_COMPLETED

        if box_left_target:
            reward += config.BOX_OFF_TARGET

        return reward

    def _apply_action(self, action):

        new_row = self.player_row + DIRECTIONS[action][0]
        new_col = self.player_col + DIRECTIONS[action][1]

        if not Board.is_valid_move(new_row, new_col, self.board, action):
            return False, False, False, True, False

        self.board, moved, pushed_box, box_on_target, box_left_target = Board.move_player(
            new_row,
            new_col,
            self.board,
            action
        )

        if moved:
            self.player_row = new_row
            self.player_col = new_col

        return moved, pushed_box, box_on_target, False, box_left_target
    

    def _get_info(
        self,
        completed=False,
        deadlock=False,
        invalid_move=False
        ):

        return {
            "level": self.level_id,
            "steps": self.steps,
            "completed": completed,
            "deadlock": deadlock,
            "invalid_move": invalid_move,
            "total_reward": self.total_reward
        }