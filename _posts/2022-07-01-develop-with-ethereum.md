---
layout:     post
title:      "以太坊开发入门"
date:       "2022-07-01 09:46:00"
author:     "Vincent"
header-img:  "img/post-bg-blockchain.jpg"
catalog: true
tags:
    - blockchain
    - Eth
    - Ethereum
---

## 背景

以太坊，英文全称 Ethereum，是一个全球协作的开源区块链项目。 该项目流通的加密货币称为以太币 (Ether)，是全球仅次于比特币的第二大流通加密货币。 它最大的特色是具有一个运行时环境：以太坊虚拟机 (Ethereum Virtual Machine,简称 EVM)， 为大规模分布式开放应用提供了运行的平台。我们可以在以太坊的虚拟机上开发智能合约实现NFT等一系列基于区块链的功能.

## 启动私链

#### 安装Geth

Geth是官方使用Golang实现的一个客户端,还有一些其他的客户端,参考 [https://ethereum.org/zh/developers/docs/nodes-and-clients/](https://ethereum.org/zh/developers/docs/nodes-and-clients/)

Geth客户端包含客户端命令行、面向网络的功能以及EVM虚拟机。 除了不能编译二进制 EVM 代码外，几乎能够执行一切和用户相关、网络相关、合约相关的操作。它承接了客户对于以太坊区块链的操作，对内维持了账户体系，世界状态，虚拟机运行以及数据的存储，对外与其他网络中的客户端节点通信，交换信息。是我们进行以太坊区块链开发的基础.

从官方网站 [https://geth.ethereum.org/downloads/](https://geth.ethereum.org/downloads/) 下载并安装Geth.(可能需要翻墙)

也可以使用Docker跑一个容器来运行Geth,官方镜像地址 [https://hub.docker.com/r/ethereum/client-go](https://hub.docker.com/r/ethereum/client-go). 后面我们使用容器来跑我们的开发环境.

#### 启动Geth

```sh
docker run -it --rm --name eth   ethereum/client-go
```

执行后就启动了节点:

```sh
INFO [07-01|03:33:50.976] Starting Geth on Ethereum mainnet...
INFO [07-01|03:33:50.978] Bumping default cache on mainnet         provided=1024 updated=4096
INFO [07-01|03:33:50.987] Maximum peer count
...
INFO [07-01|03:35:13.367] IPC endpoint opened                      url=/root/.ethereum/geth.ipc
....
```

可以新开一个终端 执行一些命令:

```sh
docker exec -it eth sh
# geth version
# geth help
```




#### 配置私链

公链和测试链会下载一堆数据,我们还是建立个私链来玩玩.

建立一个目录来存放私链数据 ```mkdir ~/data/eth/private_net_2```  
建立数据目录 ```mkdir ~/data/eth/private_net_2/db```  
建立创世块配置 ```touch ~/data/eth/private_net_2/gensis.json```  

##### gensis.json

```js

{
    "config": {
        "chainId": 18622,
        "homesteadBlock": 0,
        "eip150Block": 0,
        "eip155Block": 0,
        "eip158Block": 0
    },
    "difficulty": "0x400",
    "gasLimit": "0xffffffff",
    "coinbase": "0x0000000000000000000000000000000000000000",
    "extraData": "0x00",
    "nonce": "0x0000000000000001",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "timestamp": "0x00",
    "alloc": {
      "41835237711e43bab9e0b70dd8425f6fe7867213": {"balance": "111111"},
      "c40e24f1ae49fda0c6e7bd243337e0f43ac0ad81": {"balance": "999999"},
      "6789820778cbf30c50974a799c725bbb36c5a66e": {"balance": "600000"},
      "c848b72d24e2733c00dc8262366ed633228430b8": {"balance": "600000"}
    }
  }

```

> networkId 和 chainId
> 在以太坊网络中通常networkId和chainId设置为相同值,但是他们的用处确不相同.P2P节点之间的通讯会使用networkId ,而在交易签名处理时则使用chainId.(EIP-155在交易过程用于防止重放攻击)
> 默认networkId会使用genesis.json文件中配置的chainId
> 

初始化创世配置 

```sh
geth --datadir "./db" init gensis.json
INFO [07-01|15:49:51.259] Maximum peer count                       ETH=50 LES=0 total=50
...
INFO [07-01|15:49:51.909] Writing custom genesis block
INFO [07-01|15:49:51.910] Persisted trie from memory database      nodes=5 size=743.00B time="347.017µs" gcnodes=0 gcsize=0.00B gctime=0s livenodes=1 livesize=0.00B
INFO [07-01|15:49:51.911] Successfully wrote genesis state         database=lightchaindata hash=5f8268..28b0a4
```

### 启动私有链

```sh
docker run -it --rm --name eth -v /Users/vincentmi/data/eth/private_net_2:/root \
-p 8545:8545  \
-p 8546:8546 \
-p 30303:30303 \
-p 30304:30304 \
ethereum/client-go  --datadir /root \
--http --http.addr=127.0.0.1 --http.port 8545 --http.corsdomain "*" \
--http.api "eth,net,web3,personal,admin,shh,txpool,debug,miner" \
--nodiscover --maxpeers 30 --networkid 198989 --port 30303 \
--mine --miner.threads 1 \
--miner.etherbase "0x5e00b4e110975f62414aae1f7ef9a959cb4782b7" \
console

#命令行
geth \
--datadir  /Users/vincentmi/data/eth/private_net_2 \
--http --http.addr=127.0.0.1 --http.port 8545 --http.corsdomain "*" \
--http.api "eth,net,web3,personal,admin,shh,txpool,debug,miner" \
--nodiscover --maxpeers 30 --networkid 198989 --port 30303 \
--mine --miner.threads 1 \
--miner.etherbase "0x5e00b4e110975f62414aae1f7ef9a959cb4782b7" \
console

```


#### 连接私链

```sh
geth \
--datadir  /Users/vincentmi/data/eth/private_net_2 \
attach ipc:/Users/vincentmi/data/eth/private_net_2/geth.ipc
```

#### 查看挖矿账户收益
```sh

 web3.fromWei(eth.getBalance('0x5e00b4e110975f62414aae1f7ef9a959cb4782b7'), "ether")
 ```

#### 创建账户

```sh
> personal.newAccount('111')
INFO [07-02|09:31:56.306] Your new key was generated               
address=0xC43A7efC02e50eb04d8BEbe74c9A2FB7563A9329
0xc43a7efc02e50eb04d8bebe74c9a2fb7563a9329
> miner.setEtherbase(eth.accounts[0]) //设置挖矿奖励账户
> web3.fromWei(eth.getBalance('0x51009778ffdcc26094b58b2ac9e0ae6ab1e60ca1'), "ether") //查看奖励金额
35
```

#### 转账




