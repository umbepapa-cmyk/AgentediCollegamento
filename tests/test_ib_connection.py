"""Tests for IB connection module."""
import pytest
from unittest.mock import Mock, MagicMock
from src.ib_connection import IBConnection


def test_ib_connection_initialization():
    """Test IB connection initialization."""
    conn = IBConnection(host='127.0.0.1', port=4002, client_id=1)
    
    assert conn.host == '127.0.0.1'
    assert conn.port == 4002
    assert conn.client_id == 1
    assert not conn.is_connected()


def test_create_forex_contract():
    """Test forex contract creation."""
    conn = IBConnection()
    contract = conn.create_forex_contract('EUR.USD', 'IDEALPRO')
    
    assert contract.symbol == 'EUR'
    assert contract.secType == 'CASH'
    assert contract.exchange == 'IDEALPRO'
    assert contract.currency == 'USD'


def test_create_forex_contract_different_pair():
    """Test forex contract creation with different pair."""
    conn = IBConnection()
    contract = conn.create_forex_contract('GBP.JPY', 'IDEALPRO')
    
    assert contract.symbol == 'GBP'
    assert contract.currency == 'JPY'
