screen sample_glitch:
    vbox:
        spacing 10
        glitch:
            text "这里是一个简单的示例"

        text "\ndensity 参数为 shader 的密度"
        hbox:
            spacing 50
            glitch:
                density 5.0
                text "此时密度为 5.0"
            glitch:
                density 2.0
                text "此时密度为 2.0"
            glitch:
                density 1.0
                text "此时密度为 1.0"
            glitch:
                density 0.5
                text "此时密度为 0.5"
            glitch:
                density 0.1
                text "此时密度为 0.1"
            glitch:
                density 0.03
                text "此时密度为 0.03"

        text "\nintensity 参数为 shader 的强度"
        hbox:
            spacing 50
            glitch:
                intensity 5.0
                text "此时强度为 5.0"
            glitch:
                intensity 2.0
                text "此时强度为 2.0"
            glitch:
                intensity 1.0
                text "此时强度为 1.0"
            glitch:
                intensity 0.5
                text "此时强度为 0.5"
            glitch:
                intensity 0.1
                text "此时强度为 0.1"
            glitch:
                intensity 0.03
                text "此时强度为 0.03"

        text "\ndispersion 参数为 shader 的色散的强度"
        hbox:
            spacing 50
            glitch:
                dispersion 5.0
                text "此时强度为 5.0"
            glitch:
                dispersion 2.0
                text "此时强度为 2.0"
            glitch:
                dispersion 1.0
                text "此时强度为 1.0"
            glitch:
                dispersion 0.5
                text "此时强度为 0.5"
            glitch:
                dispersion 0.1
                text "此时强度为 0.1"
            glitch:
                dispersion 0.03
                text "此时强度为 0.03"

        text "\nalways_update 参数为 True (默认) 时会实时刷新, False 时只有当前组件被要求更新时才会更新\n然而, 现在屏幕上由于大多数组件都在更新, 没法对照了"


        text "\nlimit 参数为 True (默认) 时会按子组件的大小进行形变 (同时也会截掉色散到外部的区域), 否则按照 glitch 组件的大小进行形变, 例如:"
        
        vbox:
            spacing 10

            glitch:
                xsize 960
                ysize 50
                text "这里的 limit 为 True"
            
            glitch:
                xsize 960
                ysize 50
                limit False
                text "这里的 limit 为 False"

            fixed:
                glitch:
                    xsize 960
                    ysize 150
                    
                    text "这里的 limit 为 True"
                    text "但因为有多个子组件, 此 glitch 下的所有子组件会被装入到同一个 fixed 里(底层是这样写的), 所以色散会按照 fixed 的大小进行截取" ypos 50

                glitch:
                    xsize 960
                    ysize 150
                    xpos 960
                    limit False
                    text "这里的 limit 为 False"
                    text "也同样是因为有多个子组件, 此 glitch 下的子组件会被装入到一个 fixed 里, 但此时截取的大小为 Glitch 的大小而不是 fixed 的大小了" ypos 50


define rem = Character("Rem")


label sample_glitch_transform:
    show rem at center
    with glitch
    rem "中"

    show rem at left
    with glitch
    rem "左"

    show rem at right
    with glitch
    rem "右"

    return
