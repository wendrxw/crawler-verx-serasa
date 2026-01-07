import pytest
from unittest.mock import MagicMock
import pandas as pd
from src.driver import Handler


@pytest.fixture
def handler():
    h = Handler.__new__(Handler)  # bypass __init__
    h.logger = MagicMock()
    h.driver = MagicMock()
    return h


def test_extract_parses_table_correctly(handler):
    html = """
    <table>
        <tbody>
            <tr>
                <td>1</td>
                <td>AAPL</td>
                <td>Apple Inc.</td>
                <td>-</td>
                <td>189.00</td>
            </tr>
            <tr>
                <td>2</td>
                <td>MSFT</td>
                <td>Microsoft</td>
                <td>-</td>
                <td>420.50</td>
            </tr>
        </tbody>
    </table>
    """

    handler.driver.page_source = html

    results = handler.extract()

    assert len(results) == 2
    assert results[0]["symbol"] == "AAPL"
    assert results[1]["price"] == "420.50"


def test_pagination_returns_false_when_disabled(handler):
    btn = MagicMock()
    btn.is_enabled.return_value = False

    handler.driver.find_elements.return_value = ["cell"]
    handler.driver.execute_script = MagicMock()

    handler.driver.find_element = MagicMock(return_value=btn)

    assert handler.pagination() is False


def test_run_collects_multiple_pages(handler):
    handler.extract = MagicMock(
        side_effect=[
            [{"symbol": "A"}],
            [{"symbol": "B"}],
        ]
    )

    handler.pagination = MagicMock(
        side_effect=[True, False]
    )

    results = handler.run()

    assert len(results) == 2
    assert results[0]["symbol"] == "A"
    assert results[1]["symbol"] == "B"


def test_load_as_csv_creates_file(tmp_path, handler):
    data = [
        {"symbol": "AAPL", "name": "Apple", "price": "100"},
        {"symbol": "MSFT", "name": "Microsoft", "price": "200"},
    ]

    handler.now = "test"
    handler.load_as_csv(data)

    df = pd.read_csv("stocks_test.csv")

    assert len(df) == 2
    assert list(df.columns) == ["symbol", "name", "price"]