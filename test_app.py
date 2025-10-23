import pytest 
from dash.testing.application_runners import import_app


def test_header_present(dash_duo):
    """

    Test that the header 'Soul Foods Pink Morsel Sales Dashboard' is present
    """

    app = import_app("app")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("h1", timeout=10)

    header = dash_duo.find_element("h1")
    assert "Soul Foods Pink Morsel Sales Dashboard" in header.text

    print("✓ Header test passed!")


def test_visualization_present(dash_duo):
    """
    
    Test that the sales line chart visualization is present
    """

    app = import_app("app")
    dash_duo.start_server(app)

    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None
    
    print("✓ Visualization test passed!")


def test_region_picker_present(dash_duo):
    """
    Test that the region picker (radio buttons) is present
    """

    app = import_app("app")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-filter", timeout=10)
    
    region_filter = dash_duo.find_element("#region-filter")
    assert region_filter is not None

    radio_items = dash_duo.find_elements("#region-filter input")
    
    assert len(radio_items) == 5

    print("✓ Region picker test passed!")
