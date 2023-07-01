---
layout:     post
title:      "以太坊开发入门 - 实现ERC20合约"
date:       "2022-07-06 00:36:00"
author:     "Vincent"
image:  "img/post-bg-blockchain.jpg"
catalog: true
tags:
    - blockchain
    - Eth
    - Ethereum
    - EVM
    - ERC20
---

## Truffle和ganache

Truffle提供一个集成环境以简化合约的开发以及进行工程化.genache-cli则提供一个模拟的链上环境以便我们可以方便的进行测试.测试完成后再部署到私链或者测试链进行真正的测试和验证.提高我们的开发效率

#### 安装
开始之前请升级到较新的node版本

```sh
npm install –g truffle
npm install ganache --global
```

使用truffle 可以方便的创建模板项目

```sh
truffle unbox metacoin
```



#### truffle常用命令

编译项目

```sh
truffle compile
truffle compile --all #全部重新编译
```

部署项目

```sh
truffle migrate 
```
执行测试

```sh
truffle test 
```

>
> 如果truffle 无法连接ganache检查下truffle-config.js文件的配置
> 有时候需要把配置的名称改成 ```development```
>

## ERC20 合约

[ERC20代币标准](https://ethereum.org/zh/developers/docs/standards/tokens/erc-20/)

ERC20 通证标准（ERC20 Token Standard）是通过以太坊创建通证时的一种规范。 按照ERC20 的规范可以编写一个智能合约，创建“可互换通证”。 它并非强制要求，但遵循这个标准，所创建的通证可以与众多交易所、钱包等进行交互，它现在已被行业普遍接受。

#### 创建空白项目

```sh
mkdir erc20-test
cd erc20-test
truffle  init
```
####  ERC20Basic

```sol
pragma solidity ^0.4.24;

/**
 * @title ERC20Basic
 * @dev Simpler version of ERC20 interface.
 * See https://github.com/ethereum/EIPs/issues/179
 */
contract ERC20Basic {
    // 公开查询合约发行Token总量.
    function totalSupply() public view returns (uint256);
    // 公开查询合约中某地址所持有的Token总量
    function balanceOf(address _who) public view returns (uint256);
    // 直接转账Token的函数。由转账发起方负责呼叫此函数
    function transfer(address _to, uint256 _value) public returns (bool);
    // 转账完成后产生的事件日志
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value
    );
}
```

####  ERC20

```sol
pragma solidity ^0.4.24;

import "./ERC20Basic.sol";
/**
 * @title ERC20 interface
 * @dev Enhanced interface with allowance functions.
 * See https://github.com/ethereum/EIPs/issues/20
 */
contract ERC20 is ERC20Basic {
    // 查询授权情况.
    function allowance(address _owner, address _spender) public view returns (uint256);

    // 从授权金额中划走金额.
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool);

    // 调用方授权指定地址金额
    function approve(address _spender, uint256 _value) public returns (bool);

    // 授权发生时的日志
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
}

```

#### 使用 SafeMath基础数学库

为了防止运算溢出需要使用 SafeMath 库

```sol
pragma solidity ^0.4.24;

/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {
    /**
    * @dev Multiplies two numbers, throws on overflow.
    */
    function mul(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
      // Gas optimization: this is cheaper than asserting 'a' not being zero, but the
      // benefit is lost if 'b' is also tested.
      // See: https://github.com/OpenZeppelin/openzeppelin-solidity/pull/522
        if (_a == 0) {
            return 0;
        }

        c = _a * _b;
        assert(c / _a == _b);
        return c;
    }

    /**
    * @dev Integer division of two numbers, truncating the quotient.
    */
    function div(uint256 _a, uint256 _b) internal pure returns (uint256) {
        // assert(_b > 0); // Solidity automatically throws when dividing by 0
        // uint256 c = _a / _b;
        // assert(_a == _b * c + _a % _b); // There is no case in which this doesn't hold
        return _a / _b;
    }

    /**
    * @dev Subtracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    */
    function sub(uint256 _a, uint256 _b) internal pure returns (uint256) {
        assert(_b <= _a);
        return _a - _b;
    }

    /**
    * @dev Adds two numbers, throws on overflow.
    */
    function add(uint256 _a, uint256 _b) internal pure returns (uint256 c) {
        c = _a + _b;
        assert(c >= _a);
        return c;
    }
}
```