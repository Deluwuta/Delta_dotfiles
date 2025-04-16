#
# ░▀▄░▄▀░█▀▄▀█░▄▀▀▄░█▀▀▄░█▀▀▄░█▀▄░░░█▀▀▄░█░▒█░▀█▀░░░█▀▀▄░█▀▀▄░█▀▄
# ░░▒█░░░█░▀░█░█░░█░█░▒█░█▄▄█░█░█░░░█▀▀▄░█░▒█░░█░░░░█▀▀▄░█▄▄█░█░█
# ░▄▀▒▀▄░▀░░▒▀░░▀▀░░▀░░▀░▀░░▀░▀▀░░░░▀▀▀▀░░▀▀▀░░▀░░░░▀▀▀▀░▀░░▀░▀▀░
#
# Ye
#

import os, re, socket, subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.config import EzKey as Key
from libqtile.lazy import lazy
from libqtile.log_utils import logger

from theme import themes
theme = themes.get("biscuit_dark")

from qbar import main_bar_widgets, secondary_bar_widgets, widget_defaults, extension_defaults

# Home variable
home = os.path.expanduser('~')

# Functions for the widgets. If Qtile does not do it, I will, lol
## Volume
def get_current_volume():
    result = subprocess.run(
        ["amixer", "-D", "pulse", "get", "Master"],
        capture_output = True,
        text = True,
    ).stdout

    volume = int(result.split("[")[1].split("%")[0])
    muted = "off" in result # Check if muted

    return volume, muted

@lazy.function
def volume_update(qtile, vol_box, action="get"):
    try:
        # Define the command based on action
        base_command = ["amixer", "-D", "pulse", "set", "Master"]
        if action == "up":
            command = base_command + ["2%+", "unmute"]

        elif action == "down":
            command = base_command + ["2%-", "unmute"]

        elif action == "mute":
            command = base_command + ["toggle"]

        else:
            command = ["amixer", "-D", "pulse", "get", "Master"]

        if command:
            subprocess.run(command, stdout = subprocess.DEVNULL,
                           stderr = subprocess.DEVNULL)

        # Parse the output to find the current volume level
        volume, muted = get_current_volume()

        # Update the widget
        if vol_box in qtile.widgets_map:
            volume = "Muted" if muted else volume
            qtile.widgets_map[vol_box].update(f"Vol: {volume}%")
        else:
            logger.warning(f"Widget {vol_box} not found!")

    except Exception as e: 
        logger.warning(f"Error updating volume widget {vol_box}: {e}")

mod = "mod4"
alt = "mod1"
terminal = "alacritty" 
file_manager = "dolphin"
# launcher = "dmenu_run"
launcher = "rofi -show drun"

keys = [
    # Quit and Restart
    Key("M-C-q", lazy.shutdown()),
    Key("M-C-r", lazy.reload_config()),

    # Killin
    Key("M-S-c", lazy.window.kill()),

    Key("M-<Return>", lazy.spawn(terminal)),
    Key("M-p", lazy.spawn(launcher)),
    Key("M-f", lazy.spawn(file_manager)),

    # Multimedia
    ## Audio
    Key("<XF86AudioRaiseVolume>", volume_update(vol_box="vol_box", action="up")),
    Key("<XF86AudioLowerVolume>", volume_update(vol_box="vol_box", action="down")),

    # Change Keyboard Layout
    # Key("M-space", lazy.spawn(home + "/.config/scripts/keyboardChanger.sh")),

    # Switch between windows
    Key("M-h", lazy.layout.left() , desc="Move focus to left"),
    Key("M-l", lazy.layout.right(), desc="Move focus to right"),
    Key("M-j", lazy.layout.down() , desc="Move focus down"),
    Key("M-k", lazy.layout.up()   , desc="Move focus up"),
    Key("M-<Space>", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key("M-S-h", lazy.layout.shuffle_left() , desc="Move window to the left"),
    Key("M-S-l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key("M-S-j", lazy.layout.shuffle_down() , desc="Move window down"),
    Key("M-S-k", lazy.layout.shuffle_up()   , desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key("M-C-h", lazy.layout.grow_left() , desc="Grow window to the left"),
    Key("M-C-l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key("M-C-j", lazy.layout.grow_down() , desc="Grow window down"),
    Key("M-C-k", lazy.layout.grow_up()   , desc="Grow window up"),
    Key("M-n"  , lazy.layout.normalize() , desc="Reset all window sizes"),

    # Toggle between different layouts as defined below
    Key("M-C-<Tab>", lazy.next_layout(), desc="Toggle between layouts"),
    Key("M-m", lazy.window.toggle_fullscreen()),
    Key("M-t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            f"C-A-{vt}",
            # ["control", "mod1"], f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# groups = [Group(i) for i in "123456789"]
groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7",]
# α, β, γ, Δ, ε, ζ, η, θ, λ, μ, π, ρ, Σ, τ, φ, Ψ, Ω.
group_labels = ["α", "β", "γ", "Δ", "μ", "π", "Ω", ]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", ]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                f"M-{i.name}",
                # [mod],
                # i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = move focused window to group
            Key(
                f"M-S-{i.name}",
                # [mod, "shift"],
                # i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                f"M-C-{i.name}",
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

default_layout_theme = {
    "margin" : 6,
    "border_width" : 3,

    "single_border_width": 3,
    "single_margin": 6,

    "border_focus": theme["green"],
    "border_normal": theme["bg_dim"] 
}

layouts = [
    layout.MonadTall(
        align = 0,
        **default_layout_theme
    ),
    layout.MonadWide(**default_layout_theme),
    layout.Max(),
    layout.Floating(
        border_focus = theme["yellow"]
    )
]

def status_bar(widgets):
    return bar.Bar(
        widgets,
        24,
        opacity=1,
        background=theme["bg_dark"],
        foreground=theme["fg_normal"],
    )

screens = [
    Screen(top=status_bar(main_bar_widgets)),
    Screen(top=status_bar(secondary_bar_widgets)),
]

### To add new bars only when necessary
# xrandr = "xrandr | grep -w 'connected' | cut -d ' ' -f 2 | wc -l"
#
# command = subprocess.run(
#     xrandr,
#     shell=True,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
# )
#
# if command.returncode != 0:
#     error = command.stderr.decode("UTF-8")
#     logger.error(f"Failed counting monitors using {xrandr}:\n{error}")
#     connected_monitors = 1
# else:
#     connected_monitors = int(command.stdout.decode("UTF-8"))
#
# if connected_monitors > 1:
#     for _ in range(1, connected_monitors):
#         screens.append(Screen(top=status_bar(secondary_bar_widgets)))

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

@hook.subscribe.startup_once
def start_once():
    subprocess.call([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.startup
def initialize_volume_widget():
    volume, _ = get_current_volume()
    qtile.widgets_map["vol_box"].update(f"Vol: {volume}%")
 
# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
