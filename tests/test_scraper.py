import os
import pytest
from app.scraper import Scraper
from unittest.mock import Mock

BASE_URL = "https://dentalstall.com/shop/"

@pytest.fixture
def scraper():
    return Scraper(base_url=BASE_URL, pages=1)

def test_scrape(scraper, mocker):
    # Mock Response
    with open('tests/sample-page.html', 'r') as file:
        html_content = file.read()
    
    mock_response = Mock()
    mock_response.text = html_content
    mocker.patch('app.scraper.Scraper.fetch_page', return_value=mock_response)

    # Call Function
    products = scraper.scrape()

    # Assert The results
    assert len(products) > 0
    assert "product_title" in products[0].dict()
    assert "product_price" in products[0].dict()
    assert "path_to_image" in products[0].dict()
    
    # Delete the files created in code
    if os.path.exists("products.json"):
        os.remove("products.json")