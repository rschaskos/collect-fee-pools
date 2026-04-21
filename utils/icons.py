from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from pathlib import Path

ICONS_DIR = Path(__file__).parent.parent / "assets" / "icons"

ICON_MAPPING = {
    "plus": "plus",
    "edit": "edit-2",
    "trash": "trash-2",
    "dollar": "dollar-sign",
    "chart": "bar-chart-3",
    "trending": "trending-up",
    "zap": "zap",
    "gem": "gem",
    "keyboard": "keyboard",
    "github": "github",
    "alert": "alert-triangle",
    "waves": "waves",
}

def get_icon(key: str) -> QIcon:
    """Get icon by key from ICON_MAPPING"""
    icon_name = ICON_MAPPING.get(key)
    if not icon_name:
        return QIcon()

    icon_path = ICONS_DIR / f"{icon_name}.svg"
    if icon_path.exists():
        return QIcon(str(icon_path))
    return QIcon()
