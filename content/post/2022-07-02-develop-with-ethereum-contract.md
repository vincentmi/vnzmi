---
layout:     post
title:      "以太坊开发入门 - 智能合约"
date:       "2022-07-02 09:46:00"
author:     "Vincent"
image:  "img/post-bg-blockchain.jpg"
catalog: true
tags:
    - blockchain
    - Eth
    - Ethereum
    - Contract
---

## Solidity 语言

智能合约使用[Solidity](https://soliditylang.org/)语言进行开发,

[Solidity语法参考](https://ethbook.abyteahead.com/ch8/index.html)

Solidity 语言的一些特点:

##### 没有浮点数 
使用${wei}$来规避浮点运算.

  $
  1 \times {ether} = 1 \times  10^{18}{wei}
  $

##### 指数运算符

```sol
10**18 = 10^18
```

##### 函数权限关键字在最后

函数默认是```public```
约定 ```private```修饰的函数名字前缀加上下划线 _ 

```internal``` 修饰符可以让合约继承后子合约访问该函数
```external``` 让该函数只能被外部调用者调用

```view``` 修饰符,用于标明单纯的“查勘”类型的函数，它会读取记录在区块链上的数据，但它并不修改数据，是个只读操作
```pure``` 纯粹的函数,只是进行一些内存运算
默认则认为是写数据操作


##### 函数返回值可以是多个

#####  keccak256 函数
用于生成256bit的散列

##### 使用 emit产生日志

利用日志减少遍历区块的负担

##### msg.sender 合约调用者地址

##### require和assert
- require条件检查语句如果不通过，则扣除运行到当前语句时，程序执行所花费的 gas，终止程序执行，并返回。
- assert 条件检查语句如果不通过，则视为严重错误，扣除所有的gas，终止程序执行，并返回.

##### 使用 _ 进行 Ownerable和Pauseable控制

其他语法请参考语法说明.

## 安装编译器

我们需要安装一个编译器solc.


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

使用 ```loadScript("/Users/vincentmi/work/eth/contract/output/temp.js")```将合约内容载入.

### 部署合约 

上面的JSON数据结构包含了我们部署合约需要的数据, ```contracts['sources/Vault.sol:Vault'].abi```是合约的定义信息, ```contracts['sources/Vault.sol:Vault'].bin```是合约的代码二进制信息.智能合约的部署过程也是一次普通的交易过程，我们需要将智能合约的数据整合到交易体的数据区（data），并发送出去。 一旦交易被捕获且挖矿完成，我们的合约就已经部署在了区块链上并具有了一个独一无二的地址。通过该地址我们就能和智能合约通信并调用合约的方法.

```sh
> output.contracts['sources/Vault.sol:Vault'].abi
[{
    inputs: [],
    name: "get",
    outputs: [{
        internalType: "uint256",
        name: "",
        type: "uint256"
    }],
    stateMutability: "view",
    type: "function"
}, {
    inputs: [{
        internalType: "uint256",
        name: "data",
        type: "uint256"
    }],
    name: "set",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function"
}]
```


```sh
> output.contracts['sources/Vault.sol:Vault'].bin
"6080604052348015600f57600080fd5b5060ac8061001e6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c806360fe47b11460375780636d4ce63c146049575b600080fd5b60476042366004605e565b600055565b005b60005460405190815260200160405180910390f35b600060208284031215606f57600080fd5b503591905056fea26469706673582212204cb30acaef1d56054ffdb656c07e2788eb723c95eeb4155255171050ba19561464736f6c634300080a0033"

```

#### 准备变量

```sh
var vaultAbi = output.contracts['sources/Vault.sol:Vault'].abi
var vaultContract=eth.contract(vaultAbi)
var vaultBin = '0x'+output.contracts['sources/Vault.sol:Vault'].bin
```

#### 解锁账户

```sh
#选择一个账户
web3.fromWei(eth.getBalance('0x72fe0d652a873730006fe1ebc8059a3816f9f93b'))
#挖矿的这个账户有4000多,我们就用这个来进行合约部署

personal.unlockAccount('0x72fe0d652a873730006fe1ebc8059a3816f9f93b',"111",3000)
```

#### 提交合约

```js

var vaultDeploy = {from : '0x72fe0d652a873730006fe1ebc8059a3816f9f93b',data: vaultBin ,gas: 1000000}

var vaultContractInstance = vaultContract.new(vaultDeploy)

```

可以在控制台看到产生了合约地址

```
INFO [07-05|15:29:07.026] Submitted contract creation              hash=0xcee9a8ebc7781b8d9448866ef3605b30e3377f854a1e2a8f1e63f6b7e68ce333 from=0x51009778fFdcC26094b58B2AC9E0Ae6AB1E60Ca1 nonce=6 contract=0x3828d7E57F70522c3a6e01941A821Ff2378146f5 value=0
```

合约地址为 **0x3828d7e57f70522c3a6e01941a821ff2378146f5**

打印合约信息

```js
> vaultContractInstance
{
  abi: [{
      inputs: [],
      name: "get",
      outputs: [{...}],
      stateMutability: "view",
      type: "function"
  }, {
      inputs: [{...}],
      name: "set",
      outputs: [],
      stateMutability: "nonpayable",
      type: "function"
  }],
  address: "0x3828d7e57f70522c3a6e01941a821ff2378146f5",
  transactionHash: "0xcee9a8ebc7781b8d9448866ef3605b30e3377f854a1e2a8f1e63f6b7e68ce333",
  allEvents: function bound(),
  get: function bound(),
  set: function bound()
}
```

>
> 如果打印的```address```一直为空,说明没有矿工打包你的交易.
> 可以提高 ```gas``` 后就可以了 .
>


#### 调用合约

>
> 如果出现 错误```Error: invalid opcode: SHR```,可能是因为创世区块少了 ```"byzantiumBlock": 0,```参数.您需要重新初始化链
> 

我们合约的GET方法由于没有进行交易和变更可以直接调用.此时获取到的值是  0 

```js
> vaultContractInstance.get.call()
0
```

我们发送交易来修改这个值.

```js
> vaultContractInstance.set.sendTransaction(100,{from:"0x72fe0d652a873730006fe1ebc8059a3816f9f93b" ,gas:1000000 })

"0x1b62634409d62402563ff152c9db8af4649de26bf18464b2b6db34f7a5a07a08"

# 控制台输出
INFO [07-05|17:34:11.348] Submitted transaction                    hash=0x1b62634409d62402563ff152c9db8af4649de26bf18464b2b6db34f7a5a07a08 from=0x72Fe0D652a873730006Fe1eBC8059a3816F9F93b nonce=1 recipient=0x1004838d7DFD2750470C214021E58A1252c33699 value=0

```

打印出了交易号. 再调用```vaultContractInstance.get.call()``` 获取修改后的值.

```js
> vaultContractInstance.get.call()
100
```

一个简单的智能合约已经开发完成.

