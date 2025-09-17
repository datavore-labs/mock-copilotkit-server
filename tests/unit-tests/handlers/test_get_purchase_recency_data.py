"""Unit tests for get_purchase_recency_data handler."""

from unittest.mock import MagicMock, patch

import pytest

from mock_copilotkit_server.handler.get_purchase_recency_data import (
    get_purchase_recency_data,
    handle_get_purchase_recency_data,
)


class TestGetPurchaseRecencyData:
    """Test get_purchase_recency_data function."""

    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.config")
    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.get_mock_purchase_recency_data")
    def test_get_purchase_recency_data_mock_mode(self, mock_mock_data, mock_config):
        """Test get_purchase_recency_data in mock mode."""
        mock_config.use_live_data = False
        mock_mock_data.return_value = [{"period": "0-30 Days", "count": 100, "percentage": 25.0}]

        result = get_purchase_recency_data("cookies")

        assert result == [{"period": "0-30 Days", "count": 100, "percentage": 25.0}]
        mock_mock_data.assert_called_once_with("cookies")

    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.config")
    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.get_live_purchase_recency_data")
    def test_get_purchase_recency_data_live_mode(self, mock_live_data, mock_config):
        """Test get_purchase_recency_data in live mode."""
        mock_config.use_live_data = True
        mock_live_data.return_value = [{"period": "0-30 Days", "count": 200, "percentage": 30.0}]

        result = get_purchase_recency_data("beer")

        assert result == [{"period": "0-30 Days", "count": 200, "percentage": 30.0}]
        mock_live_data.assert_called_once_with("beer")


class TestHandleGetPurchaseRecencyData:
    """Test handle_get_purchase_recency_data function."""

    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.get_purchase_recency_data")
    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.log_params")
    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.log_result")
    def test_handle_get_purchase_recency_data_success(self, mock_log_result, mock_log_params, mock_get_data):
        """Test successful handling of get purchase recency data."""
        mock_get_data.return_value = [{"period": "0-30 Days", "count": 100, "percentage": 25.0}]
        mock_log_result.return_value = MagicMock()

        result = handle_get_purchase_recency_data("cookies")

        mock_log_params.assert_called_once_with("getPurchaseRecencyData", {"category": "cookies"})
        mock_get_data.assert_called_once_with("cookies")
        mock_log_result.assert_called_once()
        assert "data" in result
        assert "category" in result
        assert result["category"] == "cookies"

    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.get_purchase_recency_data")
    @patch("mock_copilotkit_server.handler.get_purchase_recency_data.log_params")
    def test_handle_get_purchase_recency_data_error(self, mock_log_params, mock_get_data):
        """Test error handling in get purchase recency data."""
        mock_get_data.side_effect = Exception("Test error")

        with pytest.raises(Exception, match="Test error"):
            handle_get_purchase_recency_data("cookies")

        mock_log_params.assert_called_once_with("getPurchaseRecencyData", {"category": "cookies"})
