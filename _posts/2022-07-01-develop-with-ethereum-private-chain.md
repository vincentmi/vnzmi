---
layout:     post
title:      "以太坊开发入门 - 搭建私链"
date:       "2022-07-01 09:46:00"
author:     "Vincent"
header-img:  "img/post-bg-blockchain.jpg"
catalog: true
tags:
    - blockchain
    - Eth
    - Ethereum
    - Geth
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
        "chainId": 622,
        "homesteadBlock": 0,
        "eip150Block": 0,
        "eip155Block": 0,
        "eip158Block": 0,
        "byzantiumBlock": 0,
        "constantinopleBlock": 0,
        "petersburgBlock": 0,
        "ethash": {}
    },
    "difficulty": "1",
    "gasLimit": "8000000",
    "coinbase": "0x5e00b4e110975f62414aae1f7ef9a959cb4782b7",
    "extraData": "0x00000000000000000000000000000000000000000000000000000000000000005e00b4e110975f62414aae1f7ef9a959cb4782b70000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "alloc": {
      "5e00b4e110975f62414aae1f7ef9a959cb4782b7": {"balance": "999999"},
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
--nodiscover --maxpeers 30 --networkid 622 --port 30303 \
--mine --miner.threads 1 \
--miner.etherbase "0x5e00b4e110975f62414aae1f7ef9a959cb4782b7" \
console

#命令行
geth \
--datadir  /Users/vincentmi/data/eth/private_net_2/db \
--http --http.addr=127.0.0.1 --http.port 8545 --http.corsdomain "*" \
--http.api "eth,net,web3,personal,admin,shh,txpool,debug,miner" \
--nodiscover --maxpeers 30 --networkid 622 --port 30303 \
--mine --miner.threads 1 \
--allow-insecure-unlock \
--miner.etherbase "0x5e00b4e110975f62414aae1f7ef9a959cb4782b7" \
console

```


#### 连接私链

```sh
geth \
--datadir  /Users/vincentmi/data/eth/private_net_2/db \
attach ipc:/Users/vincentmi/data/eth/private_net_2/db/geth.ipc
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

解锁账户

```sh
personal.unlockAccount(eth.accounts[0],'123',3000)
```

##### 发起转账

```sh
eth.sendTransaction({
  from: eth.accounts[0],
  to: eth.accounts[1],
  value: web3.toWei(10, 'ether')
  }
)

0x5e63fddb2995f33fbe756e980e6957ca7c4ec172a4dcdd837bc728b465cda0a7
```

执行后返回的哈希就是交易的哈希值.

此时只是发布了转账请求,交易还没有被确认,

```sh
txpool.status //查看交易状态
{
  pending: 2,
  queued: 0
}
```

查看交易内容

```js
> eth.getTransaction('0xefe7ff837428cbdc88f719bf214c5f0f3a666f7d9fe0f1896e4c4118d404d71d')
{
  blockHash: null,
  blockNumber: null,
  from: "0x51009778ffdcc26094b58b2ac9e0ae6ab1e60ca1",
  gas: 21000,
  gasPrice: 1000000000,
  hash: "0xefe7ff837428cbdc88f719bf214c5f0f3a666f7d9fe0f1896e4c4118d404d71d",
  input: "0x",
  nonce: 0,
  r: "0x812b7536609d74d184efd6fcaed7b99a3d68f5a163781922cb7352a81348faf8",
  s: "0x72794bb8053e2bce05000078761b17994c51ef071f7966ae403ae6090fdf423d",
  to: "0xc43a7efc02e50eb04d8bebe74c9a2fb7563a9329",
  transactionIndex: null,
  type: "0x0",
  v: "0x48",
  value: 10000000000000000000
}
```

##### 打包交易

```sh
miner.start(1); admin.sleepBlocks(1); miner.stop();
```

##### 查看已打包的交易

```sh
> eth.getTransaction('0xefe7ff837428cbdc88f719bf214c5f0f3a666f7d9fe0f1896e4c4118d404d71d')
{
  blockHash: "0x517c5d434fdf83806c67903a9f2cb1843e23cfa2484c054d5eef62cf50e15d97",
  blockNumber: 844,
  from: "0x51009778ffdcc26094b58b2ac9e0ae6ab1e60ca1",
  gas: 21000,
  gasPrice: 1000000000,
  hash: "0xefe7ff837428cbdc88f719bf214c5f0f3a666f7d9fe0f1896e4c4118d404d71d",
  input: "0x",
  nonce: 0,
  r: "0x812b7536609d74d184efd6fcaed7b99a3d68f5a163781922cb7352a81348faf8",
  s: "0x72794bb8053e2bce05000078761b17994c51ef071f7966ae403ae6090fdf423d",
  to: "0xc43a7efc02e50eb04d8bebe74c9a2fb7563a9329",
  transactionIndex: 0,
  type: "0x0",
  v: "0x48",
  value: 10000000000000000000
}
```

当前交易被打包到了```844```区块.

##### 查看区块信息

```sh
eth.getBlock(844)
{
  difficulty: 169043,
  extraData: "0xd983010a14846765746888676f312e31382e318664617277696e",
  gasLimit: 1882918455,
  gasUsed: 42000,
  hash: "0x517c5d434fdf83806c67903a9f2cb1843e23cfa2484c054d5eef62cf50e15d97",
  logsBloom: "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  miner: "0x51009778ffdcc26094b58b2ac9e0ae6ab1e60ca1",
  mixHash: "0x67cd6786e999f7cb6cdd09bc5eaf45e6e25e952647114e894c33f93d0f92fab1",
  nonce: "0x685fbe752776be1f",
  number: 844,
  parentHash: "0x4e332f616cbf16a63cb9667913388dd9a23e266967da2078f6e4f5f804d3af04",
  receiptsRoot: "0x0963aebd5272efe190c2582915ab9a802e7978cda7b4bcda3ee67808d06aafde",
  sha3Uncles: "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
  size: 761,
  stateRoot: "0xc3dca0428b5b75a24984a09d42fd0fa96e24f93e11c462afe5668f662c007e25",
  timestamp: 1656735556,
  totalDifficulty: 125284919,
  transactions: ["0xefe7ff837428cbdc88f719bf214c5f0f3a666f7d9fe0f1896e4c4118d404d71d", "0x5e63fddb2995f33fbe756e980e6957ca7c4ec172a4dcdd837bc728b465cda0a7"],
  transactionsRoot: "0x17d2a5f94692e77b342b7aff678af99f29882d477c20c9e630f7b25117b43b30",
  uncles: []
}
```



