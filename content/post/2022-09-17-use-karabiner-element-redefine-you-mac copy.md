---
layout:     post
title:      "用karabiner-element来定制你的MAC"
date:       "2022-09-17 22:36:00"
author:     "Vincent"
image:  "img/fix.jpg"
catalog: true
tags:
    - karabiner-element
    - MAC
---

## Logi Option

一直买罗技的鼠标搭配MAC使用, Logi Option还挺方便,但是Logi鼠标用一两年要不滚轮失灵要不经常蓝牙断连.换了个Razer 尼玛连鼠标按键定义的软件都没有MAC版. 鼠标厂商已经躺平了么. 硬件厂商不思进取又得研究下 karabiner-element.

## 安装

官网 : [https://karabiner-elements.pqrs.org/](https://karabiner-elements.pqrs.org/)

可视化映射规则配置 : [karabiner-complex-rules-generator](https://genesy.github.io/karabiner-complex-rules-generator)

## Razer DA V2X 规则

> 1. ```btn5_alfred``` 将鼠标键 button5 映射成 Left_Option + Spacebar 用于打开Alfred
> 2. ```btn4_lunch_app``` 打开lunchpad

```js
{
  "title": "VNZ_MOUSE_DEFINE",
  "rules": [
    {
      "description": "DA_V2_X_btn5_alfred",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "pointing_button": "button5"
          },
          "conditions": [
            {
              "type": "device_if",
              "identifiers": [
                {
                  "vendor_id": 1678,
                  "product_id": 157,
                  "is_pointing_device": true
                }
              ]
            }
          ],
          "to": [
            {
              "repeat": false,
              "modifiers": [
                "left_alt"
              ],
              "key_code": "spacebar"
            }
          ]
        }
      ]
    },
    {
      "description": "DA_V2_X_btn4_lunch_app",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "pointing_button": "button4"
          },
          "conditions": [
            {
              "type": "device_if",
              "identifiers": [
                {
                  "vendor_id": 1678,
                  "product_id": 157,
                  "is_pointing_device": true
                }
              ]
            }
          ],
          "to": [
            {
              "repeat": false,
              "key_code": "launchpad"
            }
          ]
        }
      ]
    },
    {
      "description": "LOGI_M590_btn5_alfred",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "pointing_button": "button5"
          },
          "conditions": [
            {
              "type": "device_if",
              "identifiers": [
                {
                  "vendor_id": 1133,
                  "product_id": 45083,
                  "is_pointing_device": true
                }
              ]
            }
          ],
          "to": [
            {
              "repeat": false,
              "modifiers": [
                "left_alt"
              ],
              "key_code": "spacebar"
            }
          ]
        }
      ]
    },
    {
      "description": "LOGI_M590_btn4_lunch_app",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "pointing_button": "button4"
          },
          "conditions": [
            {
              "type": "device_if",
              "identifiers": [
                {
                  "vendor_id": 1133,
                  "product_id": 45083,
                  "is_pointing_device": true
                }
              ]
            }
          ],
          "to": [
            {
              "repeat": false,
              "key_code": "launchpad"
            }
          ]
        }
      ]
    }
  ]
}
```



####  FOR ALL Device

```json
{
  "title": "VNZ_MOUSE_DEFINE_FOR_ALL",
  "rules": [
    {
      "description": "btn5_alfred",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "pointing_button": "button5"
          },
          "to": [
            {
              "repeat": false,
              "modifiers": [
                "left_alt"
              ],
              "key_code": "spacebar"
            }
          ]
        }
      ]
    },
    {
      "description": "btn4_lunch_app",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "pointing_button": "button4"
          },
          "to": [
            {
              "repeat": false,
              "key_code": "launchpad"
            }
          ]
        }
      ]
    }
  ]
}
```
