"""Unit tests for get_spending_data handler."""

from unittest.mock import MagicMock, patch

import pytest

from mock_copilotkit_server.handler.get_spending_data import (
    SpendingData,
    get_spending_data,
    handle_get_spending_data,
)


class TestSpendingData:
    """Test SpendingData model."""

    def test_spending_data_model(self):
        """Test SpendingData model creation and computed fields."""
        data = [{"range": "$0-10", "count": 100, "percentage": 25.0}]
        selected_brands = ["Oreo", "Chips Ahoy"]
        model = SpendingData(data=data, category="cookies", selected_brands=selected_brands)

        assert model.data == data
        assert model.category == "cookies"
        assert model.selected_brands == selected_brands
        assert model.chart_type == "spending_distribution"
        assert model.title == "Spending Distribution (Last 30 Days)"
        assert "cookies" in model.description
        assert "Spending patterns" in model.description

    def test_description_computation(self):
        """Test description computed field with different categories."""
        data = [{"range": "$25-50", "count": 200, "percentage": 30.0}]
        model = SpendingData(data=data, category="beer", selected_brands=["Heineken"])

        assert "beer" in model.description
        assert "Spending patterns" in model.description


class TestGetSpendingData:
    """Test get_spending_data function."""

    @patch("mock_copilotkit_server.handler.get_spending_data.config")
    @patch("mock_copilotkit_server.handler.get_spending_data.get_mock_spending_data")
    def test_get_spending_data_mock_mode(self, mock_mock_data, mock_config):
        """Test get_spending_data in mock mode."""
        mock_config.use_live_data = False
        mock_mock_data.return_value = [{"range": "$0-10", "count": 100, "percentage": 25.0}]

        result = get_spending_data("cookies")

        assert result == [{"range": "$0-10", "count": 100, "percentage": 25.0}]
        mock_mock_data.assert_called_once_with("cookies")

    @patch("mock_copilotkit_server.handler.get_spending_data.config")
    @patch("mock_copilotkit_server.handler.get_spending_data.get_live_spending_data")
    def test_get_spending_data_live_mode(self, mock_live_data, mock_config):
        """Test get_spending_data in live mode."""
        mock_config.use_live_data = True
        mock_live_data.return_value = [{"range": "$25-50", "count": 200, "percentage": 30.0}]

        result = get_spending_data("beer")

        assert result == [{"range": "$25-50", "count": 200, "percentage": 30.0}]
        mock_live_data.assert_called_once_with("beer")


class TestHandleGetSpendingData:
    """Test handle_get_spending_data function."""

    @patch("mock_copilotkit_server.handler.get_spending_data.get_spending_data")
    @patch("mock_copilotkit_server.handler.get_spending_data.log_params")
    @patch("mock_copilotkit_server.handler.get_spending_data.log_result")
    def test_handle_get_spending_data_success(self, mock_log_result, mock_log_params, mock_get_data):
        """Test successful handling of get spending data."""
        mock_get_data.return_value = [{"range": "$0-10", "count": 100, "percentage": 25.0}]
        mock_log_result.return_value = MagicMock()
        selected_brands = ["Oreo", "Chips Ahoy"]

        result = handle_get_spending_data("cookies", selected_brands)

        mock_log_params.assert_called_once_with(
            "getSpendingData", {"category": "cookies", "selected_brands": selected_brands}
        )
        mock_get_data.assert_called_once_with("cookies")
        mock_log_result.assert_called_once()
        assert "data" in result
        assert "category" in result
        assert "selected_brands" in result
        assert result["category"] == "cookies"
        assert result["selected_brands"] == selected_brands

    @patch("mock_copilotkit_server.handler.get_spending_data.get_spending_data")
    @patch("mock_copilotkit_server.handler.get_spending_data.log_params")
    def test_handle_get_spending_data_error(self, mock_log_params, mock_get_data):
        """Test error handling in get spending data."""
        mock_get_data.side_effect = Exception("Test error")
        selected_brands = ["Heineken", "Corona"]

        with pytest.raises(Exception, match="Test error"):
            handle_get_spending_data("beer", selected_brands)

        mock_log_params.assert_called_once_with(
            "getSpendingData", {"category": "beer", "selected_brands": selected_brands}
        )
