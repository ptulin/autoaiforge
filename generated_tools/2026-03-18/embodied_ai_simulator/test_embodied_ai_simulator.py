import pytest
from unittest.mock import patch, MagicMock, mock_open
from embodied_ai_simulator import EmbodiedAISimulator
import pygame

def test_initialize_environment():
    simulator = EmbodiedAISimulator(env_name='warehouse', agent_type='robot_arm')
    simulator.initialize_environment()
    assert simulator.env is not None
    assert simulator.agent['type'] == 'robot_arm'

def test_run_simulation():
    simulator = EmbodiedAISimulator(env_name='warehouse', agent_type='robot_arm')
    simulator.initialize_environment()

    with patch('pygame.display.set_mode') as mock_display:
        with patch('pygame.event.get', return_value=[MagicMock(type=pygame.QUIT)]):
            with patch('pygame.init'), patch('pygame.quit'), patch('pygame.display.set_caption'), patch('pygame.display.flip'), patch('pygame.draw.circle'), patch('pygame.time.Clock') as mock_clock:
                mock_clock.return_value.tick = MagicMock()
                simulator.run_simulation()
                mock_display.assert_called_once()

def test_save_logs():
    simulator = EmbodiedAISimulator(env_name='warehouse', agent_type='robot_arm')
    simulator.log_action("Move forward")
    simulator.log_action("Turn left")

    m = mock_open()
    with patch('builtins.open', m):
        simulator.save_logs("test_logs.txt")
        m.assert_called_once_with("test_logs.txt", 'w')
        handle = m()
        handle.write.assert_any_call("Move forward\n")
        handle.write.assert_any_call("Turn left\n")