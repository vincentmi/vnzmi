---
layout:     post
title:      "使用JAVA SpringBoot 构建MCP服务"
date:       "2026-09-22 15:19:00"
author:     "Vincent"
image:      "/img/leaf.jpg"
tags:
    - spring
    - java
    - AI
    - MCP
---

## 模型上下文协议（MCP, Model Context Protocol）
模型上下文协议（MCP, Model Context Protocol） 是一种为 AI 模型设计的通用上下文通信协议。它让模型与外部工具、数据资源和运行环境之间建立一个统一、安全、可扩展的接口。你可以把 MCP 理解为“AI 世界的 USB-C” —— 用一条标准化通道，让模型与一切外部系统互联。它支持多种传输机制以在不同环境中提供灵活性。

MCP JAVA SDK是MCP的JAVA实现，提供了MCP的JAVA SDK，可以让模型方便的使用MCP协议进行同步和异步的服务调用。 

Spring AI 提供 Starters和Java注解来提供对MCP的全面支持,可以很方便的构建MCP Server和client. 

## 架构

```mermaid
graph TD
    %% 定义全局样式，保持技术文档的专业感
    classDef default fill:#ffffff,stroke:#d1d5db,stroke-width:1px,color:#111827,font-family:monospace;
    classDef title fill:#f8fafc,stroke-width:0px,font-weight:bold,font-size:14px,color:#111827,font-family:sans-serif;
    classDef clientAccent fill:#f8fafc,stroke:#2563eb,stroke-width:1px,color:#1e293b;
    classDef serverAccent fill:#f8fafc,stroke:#0d9488,stroke-width:1px,color:#1e293b;
    classDef transportNode fill:#f3f4f6,stroke:#9ca3af,stroke-width:1px,color:#374151,font-weight:bold;

    %% MCP Client 子图
    subgraph Client ["MCP Client"]
        C_Session["MCP Session"]
        C_Transport["MCP Transport (Client)"]
    end

    %% MCP Server 子图
    subgraph Server ["MCP Server"]
        S_Session["MCP Session"]
        S_Transport["MCP Transport (Server)"]
    end

    %% 底部传输层 (作为一个独立的节点)
    Transport["Stdio | SSE | ..."]

    %% 建立连接关系 (隐藏线条，仅用于布局)
    C_Session --- C_Transport
    S_Session --- S_Transport
    
    %% 将上下连接起来 (使用虚线表示底层通信)
    C_Transport -.-> Transport
    S_Transport -.-> Transport

    %% 应用样式
    class Client,Server title;
    class C_Session,C_Transport clientAccent;
    class S_Session,S_Transport serverAccent;
    class Transport transportNode;
    
    %% 子图背景样式
    style Client fill:transparent,stroke:#2563eb,stroke-width:1px,stroke-dasharray: 4 4;
    style Server fill:transparent,stroke:#0d9488,stroke-width:1px,stroke-dasharray: 4 4;
```