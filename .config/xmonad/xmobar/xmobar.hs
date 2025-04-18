Config {
    -- Appearance
    -- font     = "FantasqueSansM Nerd Font 12"
    font        = "Ubuntu Mono Bold 12",
    bgColor     = "#1f2122",
    fgColor     = "#e4e6e7",
    position    = TopH 24,
    border      = BottomB,
    borderColor = "#1f2122",

    -- Layout
    sepChar =  "%",   -- delineator between plugin names and straight text
    alignSep = "}{",  -- separator between left-right alignment

    template = " %UnsafeStdinReader% }{ %dynnetwork% | %memory% | %battery% | %kbd% | %date% | ",

    -- General behavior
    lowerOnStart     = True,  -- send to bottom of window stack on start
    hideOnStart      = False, -- start with window unmapped (hidden)
    allDesktops      = True,  -- show on all desktops
    overrideRedirect = True,  -- set the Override Redirect flag (Xlib)
    pickBroadest     = False, -- choose widest display (multi-monitor)
    persistent       = True,  -- enable/disable hiding (True = disabled)

    -- plugins
    --   Numbers can be automatically colored according to their value.
    --   "xmobar" decides color based on a three-tier/two-cutoff system,
    --   controlled by command options:
    --
    --     --Low  --> sets the low cutoff
    --     --High --> sets the high cutoff
    --
    --     --low    --> sets the color below --Low cutoff
    --     --normal --> sets the color between --Low and --High cutoffs
    --     --high   --> sets the color above --High cutoff
    --
    --   The --template option controls how the plugin is displayed.
    --   Text color can be set by enclosing in <fc></fc> tags.
    --
    --   More info: http://projects.haskell.org/xmobar/#system-monitor-plugins.

    commands =  [
        -- Weather monitor
        Run Weather "RJTT" [ "--template",
            "<skyCondition> | <fc=#70b8ca><tempC></fc>°C | <fc=#70b8ca><rh></fc>% | <fc=#70b8ca><pressure></fc>hPa"
        ] 36000,

        -- Network activity
        Run DynNetwork [ "--template",
            "<dev>: <tx>kB/s|<rx>kB/s",
            "--Low"   , "1000", -- units: B/s
            "--High"  , "5000", -- units: B/s
            "--low"   , "darkgreen",
            "--normal", "darkorange",
            "--high"  , "darkred"
        ] 50,

        -- Cpu activity monitor
        Run MultiCpu [ "--template",
            "Cpu: <total0>%|<total1>%",
            "--Low"   , "50", -- units: %
            "--High"  , "85", -- units: %
            "--low"   , "darkgreen",
            "--normal", "darkorange",
            "--high"  , "darkred"
        ] 10,
                          
        -- Memory usage monitor
        Run Memory [ "--template",
            "Mem: <usedratio>%",
            "--Low"   , "20", -- units: %
            "--High"  , "90", -- units: %
            "--low"   , "darkgreen",
            "--normal", "darkorange",
            "--high"  , "darkred"
        ] 100,

        -- battery monitor
        Run Battery [ "--template",
            "Batt: <acstatus>",
            "--Low"   , "10",        -- units: %
            "--High"  , "80",       -- units: %
            "--low"   , "darkred",
            "--normal", "darkorange",
            "--high"  , "darkgreen",
            -- battery specific options
            "--", 
                "-o", "<left>% (<timeleft>)",        -- discharging
                "-O", "<fc=#dAA520>Charging</fc>", -- AC "on"
                "-i", "<fc=#006000>Charged</fc>"   -- charged
        ] 100,

        -- Date and time
        Run Date "%a, %d/%m - %I:%M:%S %P" "date" 10,

        -- Keyboard layout
        Run Kbd [
            ("us(intl)", "<fc=#00008B>US</fc>"),
            ("es"      , "<fc=#8B0000>ES</fc>")
        ],

        Run UnsafeStdinReader
    ]
}
