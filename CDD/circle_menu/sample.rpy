######################################
# 基础演示

screen circle_menu_sample:
    circle_menu:
        textbutton "AAA" action Function(print, 'AAA')
        textbutton "BBB" action Function(print, 'BBB')
        textbutton "CCC" action Function(print, 'CCC')
        textbutton "DDD" action Function(print, 'DDD')
        textbutton "EEE" action Function(print, 'EEE')
        textbutton "FFF" action Function(print, 'FFF')
        textbutton "GGG" action Function(print, 'GGG')
        textbutton "HHH" action Function(print, 'HHH')
        textbutton "III" action Function(print, 'III')
        textbutton "JJJ" action Function(print, 'JJJ')
        align (0.5, 0.5)


init python:
    def pack_str(func, *arg, **kwargs):
        def new_func(*args, **kwargs):
            info = str(args) + str(kwargs)
            info = info.replace("{", "{{")
            return func(info)
        return new_func


#######################################
# Callback 演示
screen circle_menu_with_monitor:
    vbox:
        align (0.0, 0.0)
        text "render callback"
        text "" as render_info size 20
        text "event callback"
        text "" as event_info  size 20
        text "motion callback"
        text "" as motion_info  size 20
        text "active callback"
        text "" as active_info size 20
        text "solve_select callback"
        text "" as solve_select_info  size 20
        text "apply_focus callback"
        text "" as apply_focus_info  size 20

    circle_menu:
        callbacks {
            "render": pack_str(render_info.set_text),
            "event": pack_str(event_info.set_text),
            "motion": pack_str(motion_info.set_text),
            "is_active": None,
            "active": pack_str(active_info.set_text),
            'solve_select': pack_str(solve_select_info.set_text),
            "apply_focus": pack_str(apply_focus_info.set_text)
            }
        textbutton "AAA" action Function(print, 'AAA')
        textbutton "BBB" action Function(print, 'BBB')
        textbutton "CCC" action Function(print, 'CCC')
        textbutton "DDD" action Function(print, 'DDD')
        textbutton "EEE" action Function(print, 'EEE')
        textbutton "FFF" action Function(print, 'FFF')
        textbutton "GGG" action Function(print, 'GGG')
        align (0.5, 0.5)
        as target



