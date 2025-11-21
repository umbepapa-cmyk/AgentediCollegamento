"""Tests for configuration module."""
import pytest
import os
from src.config import Config


def test_config_defaults():
    """Test default configuration values."""
    assert Config.IB_HOST == os.getenv('IB_HOST', '127.0.0.1')
    assert Config.IB_PORT == int(os.getenv('IB_PORT', '4002'))
    assert Config.IB_CLIENT_ID == int(os.getenv('IB_CLIENT_ID', '1'))


def test_config_validation():
    """Test configuration validation."""
    # Should not raise exception with default values
    Config.validate()


def test_config_validation_profit_target():
    """Test profit target validation."""
    original = Config.PROFIT_TARGET
    try:
        Config.PROFIT_TARGET = -0.1
        with pytest.raises(ValueError, match="PROFIT_TARGET must be positive"):
            Config.validate()
    finally:
        Config.PROFIT_TARGET = original


def test_config_validation_stop_loss():
    """Test stop loss validation."""
    original = Config.STOP_LOSS
    try:
        Config.STOP_LOSS = -0.1
        with pytest.raises(ValueError, match="STOP_LOSS must be positive"):
            Config.validate()
    finally:
        Config.STOP_LOSS = original


def test_config_validation_position_size():
    """Test position size validation."""
    original = Config.POSITION_SIZE
    try:
        Config.POSITION_SIZE = -100
        with pytest.raises(ValueError, match="POSITION_SIZE must be positive"):
            Config.validate()
    finally:
        Config.POSITION_SIZE = original
