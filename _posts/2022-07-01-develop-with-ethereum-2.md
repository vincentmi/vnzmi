---
layout:     post
title:      "以太坊开发入门 - 智能合约"
date:       "2022-07-01 09:46:00"
author:     "Vincent"
header-img:  "img/post-bg-blockchain.jpg"
catalog: true
tags:
    - blockchain
    - Eth
    - Ethereum
---

## 安装编译器

智能合约使用[Solidity](https://soliditylang.org/)语言进行开发,我们需要安装一个编译器solc.

### 使用NPM安装

```sh
npm install -g solc
```
运行 ```solcjs --help```

### 使用Docker

```sh
docker run ethereum/solc:stable --help
```

编译文件

```sh
docker run -v /local/path:/sources ethereum/solc:stable -o /sources/output --abi --bin /sources/Contract.sol
```


### 进行编译

我们创建一个最简单的合约设置一个变量和读取这个变量

```sol
//SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.10;

contract Vault {
    uint vaultData;
    function set(uint data) public {
        vaultData = data;
    }

    function get() public view returns (uint){
        return vaultData;
    }
}
```

进行编译

```sh

#docker编译
 docker run -it --rm --name=solc  -v `pwd`:/sources ethereum/solc:stable -o /sources/output --optimize  --combined-json abi,bin /sources/Vault.sol

```

编译后生成了ABI文件用于对合约进行描述.


combine.json
```js
{
  "contracts": {
    "sources/Vault.sol:Vault": {
      "abi": [
        {
          "inputs": [],
          "name": "get",
          "outputs": [
            {
              "internalType": "uint256",
              "name": "",
              "type": "uint256"
            }
          ],
          "stateMutability": "view",
          "type": "function"
        },
        {
          "inputs": [
            {
              "internalType": "uint256",
              "name": "data",
              "type": "uint256"
            }
          ],
          "name": "set",
          "outputs": [],
          "stateMutability": "nonpayable",
          "type": "function"
        }
      ],
      "bin": "6080604052348015600f57600080fd5b5060ac8061001e6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c806360fe47b11460375780636d4ce63c146049575b600080fd5b60476042366004605e565b600055565b005b60005460405190815260200160405180910390f35b600060208284031215606f57600080fd5b503591905056fea26469706673582212204cb30acaef1d56054ffdb656c07e2788eb723c95eeb4155255171050ba19561464736f6c634300080a0033"
    }
  },
  "version": "0.8.10+commit.fc410830.Linux.g++"
}
```

栏位描述

| --- | --- | 
| 名称 | 	解释 |
|type |	接口类型，默认为function，也可以是construnctor、fallback等|
|name |	方法名字|
|inputs |	接口输入参数列表，每一项都是参数名+参数类型|
|outputs |	接口输出结果列表，每一项都是返回值名+返回值类型|
|constant |	布尔值，若为true 则该接口不修改合约存储区，是只读方法|
|payable |	布尔值，标明该方法是否接受以太币|
|stateMutability |	枚举类型，为下列选项之一： pure：表明该方法只读不修改存储， 且不读取区块链状态 view：表明该方法只读不修改存储，但读取区块链状态 nonpayable：该方法不能接受以太币 payable：该方法可以接受以太币 |

生成的BIN代码即为虚拟机执行的代码.


## 合约部署

### 载入合约脚本

准备脚本 , 将上一步生成的json文件格式化后编辑保存为js文件

```js
var output = {
    "contracts": {
      "sources/Vault.sol:Vault": {
        "abi": [
          {
            "inputs": [],
            "name": "get",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          },
          {
            "inputs": [
              {
                "internalType": "uint256",
                "name": "data",
                "type": "uint256"
              }
            ],
            "name": "set",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
          }
        ],
        "bin": "6080604052348015600f57600080fd5b5060ac8061001e6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c806360fe47b11460375780636d4ce63c146049575b600080fd5b60476042366004605e565b600055565b005b60005460405190815260200160405180910390f35b600060208284031215606f57600080fd5b503591905056fea26469706673582212204cb30acaef1d56054ffdb656c07e2788eb723c95eeb4155255171050ba19561464736f6c634300080a0033"
      }
    },
    "version": "0.8.10+commit.fc410830.Linux.g++"
  }
```

使用 ```loadScript```将合约载入到Geth节点.
