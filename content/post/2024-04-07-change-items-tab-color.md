---
layout:     post
title:      "修改Items2的Tab颜色"
date:       "2024-04-07 16:26:00"
author:     "Vincent"
image:  "/img/post-bg-python.png"
catalog: true
tags:
    - items2
    - shell
    - zsh
---

# 增加一个items插件


```sh

# /Users/vincentmi/.oh-my-zsh-custom

if [[ -n "$ITERM_SESSION_ID" ]]; then
    tab-color() {
        echo -ne "\033]6;1;bg;red;brightness;$1\a"
        echo -ne "\033]6;1;bg;green;brightness;$2\a"
        echo -ne "\033]6;1;bg;blue;brightness;$3\a"
    }
    tab-red() { tab-color 255 0 0 }
    tab-green() { tab-color 0 255 0 }
    tab-blue() { tab-color 0 0 255 }
    tab-reset() { echo -ne "\033]6;1;bg;*;default\a" }

    function iterm2_tab_precmd() {
        tab-reset
    }

    # function iterm2_tab_preexec() {
    #     if [[ "$1" =~ "^ssh " ]]; then
    #         if [[ "$1" =~ "prod" ]]; then
    #             tab-color 255 160 160
    #         else
    #             tab-color 160 255 160
    #         fi
    #     else
    #         tab-color 160 160 255
    #     fi
    # }

    function iterm2_tab_preexec() {
        if [[ "$1" =~ "^ssh " ]]; then
            if [[ "$1" =~ "prod" || "$1" =~ "live"  ]]; then
                tab-color 220 20 60
            else
                if [[ "$1" =~ "qa" ]]; then
                    tab-color 255 204 153
                else
                    tab-color 160 255 160
                fi
            fi
        else
            if [[ "$1" =~ "auth" ]]; then
                tab-color 255 178 102
            else
                if [[ "$1" =~ "cv" ]]; then
                    tab-color 204 255 229
                else
                    tab-color 160 160 255
                fi
            fi
        fi
    }


    autoload -U add-zsh-hook
    add-zsh-hook precmd  iterm2_tab_precmd
    add-zsh-hook preexec iterm2_tab_preexec
fi
```