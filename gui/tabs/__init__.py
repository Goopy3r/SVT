"""
Tabs package for Network Guard GUI
"""

from gui.tabs.traffic_analytics import TrafficAnalyticsTab
from gui.tabs.blocking_controls import BlockingControlsTab
from gui.tabs.home_tab import HomeTab
from gui.tabs.blocked_items import BlockedItemsTab
from gui.tabs.advanced_controls import AdvancedControlsTab

__all__ = [
    'TrafficAnalyticsTab',
    'BlockingControlsTab',
    'HomeTab',
    'BlockedItemsTab',
    'AdvancedControlsTab'
]