---
layout:     post
title:      "Clayman的3D学习指南"
date:       2015-05-03 8:36:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - CGI
---


http://www.cnblogs.com/clayman/archive/2009/05/17/1459001.html
仅供个人学习使用，请勿转载，勿用于任何商业用途。
作者：Clayman
         与玩游戏相比,写游戏要复杂上千万倍,除了需要掌握通用的编程技巧以外，还要有相当的图形学，物理，数学基础，特别是在国内，由于相关资料的缺乏，更是让初学者无从下手。下面总结了一些入门方法和比较容易入手的资料。
         首先你要精通一门高级语言，比如C++或者C#，其次，要有良好的英文阅读能力。对游戏开发者来说英文阅读能力是最重要也是最基本的工具之一，因为你遇到的大部分资源都将是英文的，不要总等着别人为你翻译。慢慢尝试着阅读英文资料，你会发现其实也并没有那么难:)


<!--more-->


 
         刚开始，你要做的就是选择一门图形API，一般就是DirectX或者OpenGL之间选一个。如果考虑到跨平台，那么OGL是首选. 如果只在ms的平台，则DX是首选。我对OGL并不是很了解，所以下面大部门资料都是和DX相关的。当然，作为准备工作之一，你首先要到DirectX Develop Center下载最新版的DirectX SDK。
 
         入门书籍非常重要，推荐<<Introduction to 3D Game Programming with DirectX 9.0>>（好像去年出了中文版）也就是传说中的龙书，这可以说是最好的DX入门教材，Frank Luna从浅入深，讨论了DX的方方面面。另外再配上<<DirectX 9 Graphics  the Definitive Guide to Direct3D>>，书名虽然是definitive，但实际属于入门基本的书。看完这两本书，你基本上已经对DirectX比较熟悉了。如果你希望学习XNA，也是一样的，毕竟XNA是以DX为基础。
更新(2010.11.6): <<Introduction to 3D Game Programming with DirectX 9.0>>的第二版，《xxx, A Shader Approach》也可以找到了。
 
         不要一开始就看图形学的书，这个时候你对图形编程还没有一个基本的感性认识，因此八成看的云里雾里。不要以网上的教程和论坛提问作为主要学习途径，找一本好书，系统学习，效率才最高。不要马上看SDK里的例子，很多图形学的基本原理仅仅通过读代码是不会明白的。某些年代太过久远的书最好*不要*看了，比如<<windows游戏编程大师技巧>>  <<3D游戏编程大师技巧>> 。有人说基本的思想总是不变的，可惜对于现代GPU来说，很多早期的技术和优化技巧早就过时了。图形编程是发展的非常快的技术，看看GPU的发展速度，1~2年就是一代产品的革新。
 
          好了，入门之后，是你巩固和拓展视野的阶段。现在看计算机图形学就比较合适了。吐血推荐<<Real-Time-Rendering>>,这本书算得上是所有图形程序员的必读书籍和参考手册了。最近刚出了第三版（更新：已经有电子版了）。可惜国内只有第二版，稍微有点老，如果实在找不到第三版，还是值得一读。国内其他所有以图形学命名的书都有一个共同点：枯燥，过时。只需看看其中二维三维变换和曲线曲面表示的部分即可。如果这个时候发现你当年数学没有学好，那么有三本数学书是为游戏程序员量身定制的：<<3D Math Primer for Graphics and Game Development>>, <<Mathematics for 3D Game Programming and Computer Graphics>>和<<Essential Mathematics Guide 2nd Edition>>，第一本书有中文版，最后一本则是08年才出的新书。
 
更新(2010.11.6)  看完上述入门书籍之后，就应该花点时间好好的完整阅读DirectX文档以及部分sample了，加深对DX整个系统，函数的了解。你会发现普通论坛里60%的问题都是文档里讲过的。
 
         其实入门之后，就没有固定的学习路线了，最好根据你感兴趣的方向来学习。
 
Shader方面：
《Cg_tutorial》和《The Complete Effect and HLSL Guide》都是不错的入门材料，当然还有SDK文档。<<Shaders for Game Programmers and Artists>>有大量入门的例子。<<Advanced Lighting And Materials With Shaders>>详细介绍了各种光照模型和技术。<<GPU Gems>> 1~3册肯定是必读的，虽然有1，2有中文版，但某些翻译并不是很理想，强烈建议直接看英文版。ShaderX系列也是很经典的系列，每年出版一本，包含了最新的实时渲染技术，如今已经出了第6册了。不过网络上只能找到1~3册。1，2册大部分shader都是用asm写的，不过看懂原理，转换为HLSL也并不难。另外Nvidia SDK和ATI SDK也是学习shader的重要资源。最后还有刚出的<< Programming Vertex, Geometry, and Pixel Shaders>>
更新(2010.4.30):ShaderX已经出版了第7册，后续的版本由于版权原因，改名为GPU Pro: Advanced Rendering Techniques，仍然每年出版一本。
更新(2010.11.6): 天朝人民的智慧是无限的，很多图形学的新书都能在taobao买单翻印的纸版了，包括ShaderX系统等等.....
更新(2010.11.6): 关于ShaderX和GPU Gems常常有人问我较老的几册值不值得看，还有看不懂怎么办。这里是我个人的看法，仅供参考：ShaderX和GPU Gems收录的都是比较前沿的技术，虽然每本之间没有连续性，但很多技术都建立在之前的方法上。有时间的话，建议从第一本看起。两本书都属于论文集，章节之间并没有太多连续性，所以不必从第一页看到最后一页，选择你感兴趣的部分即可。比如对阴影感兴趣，就只看阴影相关的章节，你可以看到整个阴影技术近10年的发展，变化，很有价值。另外，书里很多前沿，实验性的技术，由于硬件限制，通常要2,3年后才有可能普及，现在看以前的几册也不会太"过时"。 最后，这样的书内容涉及了图形学的方法面面，2d,3d,图像处理，ai，游戏构架，gpgpu等等，范围太过广泛，特别是GPU Gems相比ShaderX更偏重学术研究，很多技术最终不一定能实际应用到产品中，有些章节看不懂也属于正常现象。
 
地形：
<<Real Time 3D Terrain Engines Using C++ And DX9>>非常全面的讨论了关于地形渲染的各种技术，至少应该把第5~9章都浏览一遍。之后便可以 到virtual terrain查阅近期的地形渲染技术。
更新(2010.11.6): 经常尝试用PIX分析你电脑上的游戏，地形渲染通常是最容易分析的部分，而且可以让你马上了解目前流行的地形渲染方法。
 
模型导入和动画：
<<Advanced Animation with DirectX>>，仅此一本足以。
更新(2010.5.5):<<Character Animation With Direct3D>>已经可以很容易的找到了, 此书介绍了目前最新的游戏动画技术，作者是xbox360大作Alan Wake的开发人员，完全可以替代上面提到的那本。
 
物理：
<<Game Physics>>和<<Game Physics Engine Development>>都不错。<<Real-time Collision Detection>>是碰撞检测方面最好的书。：<<3D Game Engine Design, 2nd>>的8,9章也值得一看。
 
LOD：
<<Level of Detail for 3D Graphics>>
 
Ray tracing:
<< Physical-Based Rendering - From Theory to Implementation>> 
更新(2010.4.30): 一本免费的入门教程Another Introduction to Ray Tracing
更新(2010.11.6): 此书已有第二版，而且某网站有翻印版出售。
 
引擎设计:
说实话，这方面还没有特别好的书，大概越是核心的内容，越少有人愿意写吧。<<3D Game Engine Architecture Engineering Real-Time Applications with Wild Magic>>只有第三章值得一读。<<3D Game Engine Programming>>可以选部分感兴趣的章节看看，不过总的来说，讲的比较浅。
更新：<<3D Game Engine Design, Second Edition>>出了影印版本，此书是<<3D Game Engine Architecture Engineering>>更新版，强烈推荐。
最近发现<<Pro OGRE 3D Programming>>也很不错，200多页短小精干，但是可以让读者快速了解一个既有引擎的设计和构架。
更新(2010.7.15): 新出的《Game Engine Architecture》非常不错，注意是Jason Gregory的版本。如果只推荐一本引擎方面的书，绝对是这本。传说有扫描电子版了。
更新(2010.6.28): <<Game Engine Gems>>是关于引擎设计的新系列丛书，与ShaderX类似，也是每年一本，目前已经出版了第一册，已有电子版
 
AI & Game Programming
<<Programming Game AI by Example>>非常不错，好像还有中文版，备选<<Artificial Intelligence for Games>>(已有第二版)。当然<<AI Programming Wisdom>>系列也是必读作品，不过目前网络上只有1～2册。
更新(2010.5.28)：<<AI Game Engine Programming>>已比较好找了，虽然说这是一本名不副实的书，并没有完全介绍一个"one for all"类型的引擎，也没有具体算法讨论，但针对各种不同类型游戏的AI设计做了详细介绍，可作为一本指参考导性书选择阅读。

网络：mai%25##&%...（本人网络白痴 +_+........)
 
综合：
<<Game Programming Gems>>系列，不过由于内容涉及的过于广泛，文章质量参差不齐，选择性阅读就可以了。历年GDC, Gamefest,Siggraph等大型会议的paper也是应该关注的。至于那些“All in one”或者n天较你写出个FPS游戏的书就不要读了，这类书的通病是什么都说了，结果什么也没说清楚。
 
除了书以外，再推荐一些不错的网络资源：
http://www.gamedev.net/ 除了大量教程以外，论坛里多年累计下来的内容保罗万象。好好利用论坛搜索，你会发不管你多厉害，那里总有一些比你强大的人在很久以前就遇到了和你同样的问题，并且给出了解决方案。
Nvidia和ATI的开发者中心
creators.xna.com  XNA官方网站
http://www.gamasutra.com/ 与GameDev类似
http://www.beyond3d.com/ 这里的除了讨论软件以外，还能看到对硬件构架的分析
http://www.gameres.com/ 国内唯一比较专业的游戏编程网站，可惜和GameDev相比就显得太寒碜了-_-#
         当然，不要忘了收集各大论坛里牛人们的blog：）
         最后，仅仅靠看书是不够的，多写多练才是王道。
 
 
ps：以上书籍，除了特别注明的以外，都是可以通过网络或者书店入手的。不要找我要电子书，我能找到的，相信你也能找到，你找不到的，我肯定也没有 :)
pps：如果你非要转这篇文章，至少应该保留原文链接和作者吧................. 



