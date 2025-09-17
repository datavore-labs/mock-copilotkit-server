"""Unit tests for get_brand_data handler."""

from unittest.mock import MagicMock, patch

import pytest

from mock_copilotkit_server.handler.get_brand_data import (
    get_brand_data,
    handle_get_brand_data,
)


class TestGetBrandData:
    """Test get_brand_data function."""

    @patch("mock_copilotkit_server.handler.get_brand_data.config")
    @patch("mock_copilotkit_server.handler.get_brand_data.get_mock_brand_data")
    def test_get_brand_data_mock_mode(self, mock_mock_data, mock_config):
        """Test get_brand_data in mock mode."""
        mock_config.use_live_data = False
        mock_mock_data.return_value = [{"brand": "Oreo", "count": 100, "percentage": 25.0}]

        result = get_brand_data("cookies")

        assert result == [{"brand": "Oreo", "count": 100, "percentage": 25.0}]
        mock_mock_data.assert_called_once_with("cookies")

    @patch("mock_copilotkit_server.handler.get_brand_data.config")
    @patch("mock_copilotkit_server.handler.get_brand_data.get_live_brand_data")
    def test_get_brand_data_live_mode(self, mock_live_data, mock_config):
        """Test get_brand_data in live mode."""
        mock_config.use_live_data = True
        mock_live_data.return_value = [{"brand": "Heineken", "count": 200, "percentage": 30.0}]

        result = get_brand_data("beer")

        assert result == [{"brand": "Heineken", "count": 200, "percentage": 30.0}]
        mock_live_data.assert_called_once_with("beer")


class TestHandleGetBrandData:
    """Test handle_get_brand_data function."""

    @patch("mock_copilotkit_server.handler.get_brand_data.get_brand_data")
    @patch("mock_copilotkit_server.handler.get_brand_data.log_params")
    @patch("mock_copilotkit_server.handler.get_brand_data.log_result")
    def test_handle_get_brand_data_success(self, mock_log_result, mock_log_params, mock_get_data):
        """Test successful handling of get brand data."""
        mock_get_data.return_value = [{"brand": "Oreo", "count": 100, "percentage": 25.0}]
        mock_log_result.return_value = MagicMock()

        result = handle_get_brand_data("cookies", "0-30 Days")

        mock_log_params.assert_called_once_with(
            "getBrandData", {"category": "cookies", "selected_recency": "0-30 Days"}
        )
        mock_get_data.assert_called_once_with("cookies")
        mock_log_result.assert_called_once()
        assert "data" in result
        assert "category" in result
        assert "selected_recency" in result
        assert result["category"] == "cookies"
        assert result["selected_recency"] == "0-30 Days"

    @patch("mock_copilotkit_server.handler.get_brand_data.get_brand_data")
    @patch("mock_copilotkit_server.handler.get_brand_data.log_params")
    def test_handle_get_brand_data_error(self, mock_log_params, mock_get_data):
        """Test error handling in get brand data."""
        mock_get_data.side_effect = Exception("Test error")

        with pytest.raises(Exception, match="Test error"):
            handle_get_brand_data("beer", "30-60 Days")

        mock_log_params.assert_called_once_with("getBrandData", {"category": "beer", "selected_recency": "30-60 Days"})
