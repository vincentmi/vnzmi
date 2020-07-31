---
layout:     post
title:      "Antd-v读取和设置后端的错误信息"
date:       "2020-07-31 23:05:00"
author:     "Vincent"
header-img:  "img/post-bg-water.jpg"
catalog: true
tags:
    - Antd
    - Vue
    - Validate
---

## 场景

最近用```Antd-v```做后台,自带的验证框架.提供了很多的前台验证方法,找了一圈没有找到结合后端验证的,比较纳闷现在前端同学都自己验证不用后端的验证信息了吗?最终的数据验证应该还是以后端为准.自己写了几个函数.

## 使用

#### 后端返回数据结构

```json
{
    code: 600412,
    msg: "数据验证失败",
    data: {
        userName: "用户名已经存在",
        email: "无效的邮箱服务商"
    }
}
```

#### 使用方式

引入插件

```js
import MiValidator from './plugins/validator'
Vue.use(MiValidator)
```
在组件中调用方式如下

```js
this.$mi.assign(this.$refs.editorForm,result.data);//设置错误信息
this.$mi.clear(this.$refs.editorForm);//清除错误信息
```

## 代码

使用这两个函数可以少写一些绑定代码.```assign```会自动查询目标表单中的栏位,根据```v-model```绑定的变量名称来识别错误信息.```form.name```会被识别为```name```,匹配服务端返回的```name```的错误信息.

```js

const MiValidator = {}
const ALLOWED_TAGS = 'a-input,a-input-password,a-select,a-switch'

MiValidator.install = function (Vue, options) {
    Vue.prototype.$mi = MiValidator
    const queryNearParent = (comp, tag) => {
        if (comp.$parent) {
            if (tag.indexOf(comp.$parent.$options._componentTag) > -1) {
                return comp.$parent
            } else {
                return queryNearParent(comp.$parent, tag)
            }
        }
        return null
    }
    // 获取引用内部可以附加错误提示的组件
    const pickValiateItems = (ref) => {
        const rootTag = ref.$options._componentTag
        // console.log(ref)
        if (rootTag !== 'a-form-model' && rootTag !== 'a-form') {
            throw new Error('you can just display validate in on a-form-model or a-form')
        }
        const children = queryChild(ref)
        const nodeMap = {}
        for (let i = 0, m = children.length; i < m; i++) {
            if (children[i].$vnode.data.model.expression) {
                const varExpression = children[i].$vnode.data.model.expression
                const index = varExpression.lastIndexOf('.')
                const key = index > -1 ? varExpression.substring(index + 1) : varExpression
                nodeMap[key] = children[i]
            }
        }
        return nodeMap
    }

    const queryChild = (comp) => {
        let children = []
        for (let i = 0, m = comp.$children.length; i < m; i++) {
            const child = comp.$children[i]
            if (child && child._isVue) {
                if (child.$children.length > 0) {
                    children = children.concat(queryChild(child))
                }
                if (ALLOWED_TAGS.indexOf(child.$options._componentTag) > -1) {
                    children.push(child)
                }
            }
        }
        return children
    }

    MiValidator.clear = (ref) => {
        const nodeMap = pickValiateItems(ref)
        for (const key in nodeMap) {
            const parent = queryNearParent(nodeMap[key], 'a-form-item,a-form-model-item')
            parent.$data.validateState = null
            parent.$data.validateMessage = null
        }
    }
    MiValidator.assign = (ref, erroInfo) => {
        const nodeMap = pickValiateItems(ref)
        for (const key in erroInfo) {
            if (nodeMap[key]) {
                const parent = queryNearParent(nodeMap[key], 'a-form-item,a-form-model-item')
                parent.$data.validateState = 'error'
                parent.$data.validateMessage = erroInfo[key]
            }
        }
    }
}

export default MiValidator

```

