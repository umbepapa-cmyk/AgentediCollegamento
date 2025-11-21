"""Tests for scalping strategy module."""
import pytest
from src.scalping_strategy import ScalpingStrategy


def test_strategy_initialization():
    """Test strategy initialization."""
    strategy = ScalpingStrategy(
        profit_target=0.0002,
        stop_loss=0.0001,
        position_size=20000
    )
    
    assert strategy.profit_target == 0.0002
    assert strategy.stop_loss == 0.0001
    assert strategy.position_size == 20000
    assert strategy.current_position is None


def test_should_enter_long_no_position():
    """Test entering long position logic."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    
    # With tight spread, should consider entry
    current_price = 1.1000
    bid = 1.0999
    ask = 1.1001
    
    # Note: actual entry depends on spread threshold
    result = strategy.should_enter_long(current_price, bid, ask)
    assert isinstance(result, bool)


def test_should_not_enter_with_existing_position():
    """Test that strategy doesn't enter when position exists."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    strategy.enter_position('LONG', 1.1000)
    
    # Should not enter another position
    assert not strategy.should_enter_long(1.1000, 1.0999, 1.1001)
    assert not strategy.should_enter_short(1.1000, 1.0999, 1.1001)


def test_enter_position():
    """Test position entry."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    strategy.enter_position('LONG', 1.1000)
    
    assert strategy.current_position is not None
    assert strategy.position_side == 'LONG'
    assert strategy.entry_price == 1.1000


def test_exit_position_profit_target_long():
    """Test exiting long position at profit target."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    strategy.enter_position('LONG', 1.1000)
    
    # Price moves up to profit target
    current_price = 1.1002  # 0.0002 profit
    should_exit, reason = strategy.should_exit_position(current_price)
    
    assert should_exit
    assert reason == "PROFIT_TARGET"


def test_exit_position_stop_loss_long():
    """Test exiting long position at stop loss."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    strategy.enter_position('LONG', 1.1000)
    
    # Price moves down to stop loss
    current_price = 1.0999  # -0.0001 loss
    should_exit, reason = strategy.should_exit_position(current_price)
    
    assert should_exit
    assert reason == "STOP_LOSS"


def test_exit_position_profit_target_short():
    """Test exiting short position at profit target."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    strategy.enter_position('SHORT', 1.1000)
    
    # Price moves down to profit target
    current_price = 1.0998  # 0.0002 profit
    should_exit, reason = strategy.should_exit_position(current_price)
    
    assert should_exit
    assert reason == "PROFIT_TARGET"


def test_exit_position_stop_loss_short():
    """Test exiting short position at stop loss."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    strategy.enter_position('SHORT', 1.1000)
    
    # Price moves up to stop loss
    current_price = 1.1001  # -0.0001 loss
    should_exit, reason = strategy.should_exit_position(current_price)
    
    assert should_exit
    assert reason == "STOP_LOSS"


def test_no_exit_within_range():
    """Test that position doesn't exit within profit/loss range."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    strategy.enter_position('LONG', 1.1000)
    
    # Price moves slightly but not to target or stop
    current_price = 1.10005  # Small profit
    should_exit, reason = strategy.should_exit_position(current_price)
    
    assert not should_exit


def test_get_position_info():
    """Test getting position information."""
    strategy = ScalpingStrategy(0.0002, 0.0001, 20000)
    
    # No position initially
    assert strategy.get_position_info() is None
    
    # After entering position
    strategy.enter_position('LONG', 1.1000)
    position_info = strategy.get_position_info()
    
    assert position_info is not None
    assert position_info['side'] == 'LONG'
    assert position_info['entry_price'] == 1.1000
