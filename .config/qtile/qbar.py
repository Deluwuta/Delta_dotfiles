import os, subprocess
from libqtile import bar, widget
from libqtile.config import Screen
from libqtile.log_utils import logger

from theme import themes
theme = themes.get("biscuit_dark")

home = os.path.expanduser('~')

widget_defaults = dict(
    font = "IntoneMonoNerdFont",
    fontsize = 16,
    padding = 4,
)
extension_defaults = widget_defaults.copy()

def workspaces():
    return [
        widget.GroupBox(
            font = "IntoneMonoNerdFont Bold",
            fontsize = 18,

            # Workspace design
            borderwidth = 2,
            highlight_method = 'line',
            highlight_color = theme["bg_normal"], # For line method

            # Letter color
            active = "#FFFFFF",
            inactive = theme["bg_light"],

            # Highlight color
            this_current_screen_border = theme["yellow"],
            this_screen_border = theme["yellow"],

            other_current_screen_border = theme["bg_normal"],
            other_screen_border = theme["bg_normal"],

            rounded = True,
            disable_drag = True,
        ),

    ]

main_bar_widgets = [
    widget.LaunchBar(
        progs = [
            (
                home + "/Pictures/nixos.png",
                "rofi -show drun",
                "Rofi Launcher",
            )
        ],
        padding_y = -1,
        padding = 8,
        icon_size = 22,
    ),

    *workspaces(),

    widget.Sep(linewidth = 1, padding = 6),

    widget.CurrentLayoutIcon(scale = 0.9, padding = 3),

    widget.Sep(linewidth = 1, padding = 6),

    widget.WindowName(),

    widget.TextBox(
        text = "No way",
        name = "vol_box",
    ),

    widget.Sep(linewidth = 1, padding = 6),

    widget.CheckUpdates(
        # colour_have_updates=theme["fg_normal"],
        # colour_no_updates=theme["fg_normal"],
        no_update_string='Pac: 0',
        display_format='Pac: {updates}',
        update_interval = 1800,
        custom_command='checkupdates',
    ),
    widget.Sep(linewidth = 1, padding = 6),

    widget.Clock(format="%A %d/%m - %H:%M"),

    widget.Sep(linewidth = 1, padding = 6),

    widget.Systray(
        padding = 8,
        icon_size = 22,
    ),
    widget.Sep(linewidth = 0),
]

secondary_bar_widgets = [
    widget.LaunchBar(
        progs = [
            (
                home + "/Pictures/nixos.png",
                "rofi -show drun",
                "Rofi Launcher",
            )
        ],
        padding_y = -1,
        padding = 8,
        icon_size = 22,
    ),

    *workspaces(),

    widget.Sep(linewidth = 1, padding = 6),

    widget.CurrentLayoutIcon(scale = 0.9, padding = 3),

    widget.Sep(linewidth = 1, padding = 6),

    widget.WindowName(),

    widget.Clock(format="%A %d/%m - %H:%M"),

    widget.Sep(linewidth = 0),
]
