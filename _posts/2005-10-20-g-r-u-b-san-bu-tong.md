---
layout:     post
title:      "grub三步通"
date:       2005-10-20 11:58:47
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: true
tags:
    - 新浪博客
    - 技术文章
---


grub三步通 


################## 
# GRUB的优点 # 
################## 
GRUB 是引导装入器(boot loader) -- 它负责装入内核并引导 Linux 系统。GRUB 还可以引导其它操作系统，如 FreeBSD、NetBSD、OpenBSD、GNU HURD 和 DOS，以及 Windows 95、98、NT 和 2000。尽管引导操作系统看上去是件平凡且琐碎的任务，但它实际上很重要。如果引导装入器不能很好地完成工作或者不具有弹性，那么就可能锁住系统，而无法引导计算机。另外，好的引导装入器可以给您灵活性，让您可以在计算机上安装多个操作系统，而不必处理不必要的麻烦。 
GRUB 是一个很棒的boot loader。它有许多功能，可以使引导过程变得非常可靠。例如，它可以直接从 FAT、minix、FFS、ext2 或 ReiserFS 分区读取 Linux 内核。这就意味着无论怎样它总能找到内核。另外，GRUB 有一个特殊的交互式控制台方式，可以让您手工装入内核并选择引导分区。这个功能是无价的：假设 GRUB 菜单配置不正确，但仍可以引导系统。哦，对了 -- GRUB 还有一个彩色引导菜单。 

更令人惊讶的是，这是一个自由软件！！！ 



################## 
# GRUB菜单 # 
################## 
先来看一个例子，这是位于/boot/grub/目录下的menu.lst文件。 
此文件将在开机是产生一个菜单，包含有Debian linux,Windows2000,RedHat linux和 Mandrake linux,共四个选择项。我一共分了8个区，一个fat16（0x6），一个ntfs（0x7），三个ext2fs分区（0x83），一个swap分区（0x82）。ntfs用来装win2000，三个ext2fs装了三个linux，c盘fat16分区没有装任何东西。 
＃例子由此开始 

＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃ 
＃ ＃ 
＃ 一个GRUB configure 的例子 ＃ 
＃ ＃ 
＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃＃ 

timeout 10 
default 2 


# --&gt; Debian linux &lt;-- 

title Debian linux 
root (hd0,2) 
kernel /boot/vmlinuz-2.2.18 root=/dev/hda3 ro 
initrd /boot/initrd-2.2.18.gz 


# --&gt; Debian END &lt;-- 

# --&gt; Windows 菜单选项 &lt;-- 

title Windows2000 
root (hd0,0) 
chainloader +1 

# --&gt; Winddows 结束 &lt;-- 

# --&gt; RedHat linux 菜单选项 &lt;-- 

title RedHat linux 
root (hd0,8) 
chainloader +1 # 在硬盘主引导分区装了lilo，所以也用了chainloader。 

# --&gt; RedHat linux 结束 &lt;-- 

# --&gt; Mandrake linux 菜单选项 &lt;-- 

title Mandrake linux 
root (hd0,5) 
kernel /boot/vmlinuz-2.4.3-20mdk root=/dev/hda6 ro 
initrd /boot/initrd-2.4.3-20mdk.img 

# --&gt; Mandrake linux 结束 &lt;-- 


＃例子到此结束 

以符号井＂＃＂开头的行表示被注释掉，没有任何意义。 

timeout表示默认等待的时间，这儿是10秒钟。超过10秒，用户还没有作出选择的话，系统将自动选择默认的操作系统。 

默认的操作系统就是由default控制的。default后加一个数字n，表明是第n＋1个。需要注意的是，GRUB中，计数是从0开始的，第一个硬盘是hd0，第一个软驱是fd0，等等。所以，default 2 表示默认的操作系统在这儿是 Redhat linux。 

接下来，正如你所想象的，title表示的是“Debian linux”菜单项。root (hd0,2)表示第一个硬盘,第三个分区。这儿的root 于linux的root分区及其不同，此root非彼root也！ 

在 Linux 中，当谈到 "root" 文件系统时，通常是指主 Linux 分区。但是，GRUB 有它自己的 root 分区定义。GRUB 的 root 分区是保存 Linux 内核的分区。这可能是您的正式 root 文件系统，也可能不是。我们讨论的是 GRUB，需要指定 GRUB 的 root 分区。进入 root 分区时，GRUB 将把这个分区安装成只读型，这样就可以从该分区中装入 Linux 内核。GRUB 的一个很“酷”的功能是它可以读取本机的 FAT、FFS、minix、ext2 和 ReiserFS 分区。 

到目前为止，您可能会感到一点疑惑，因为 GRUB 所使用的硬盘／分区命名约定与 Linux 使用的命名约定不同。在 Linux 中，第一个硬盘的第五个分区称作 "hda5"。而 GRUB 把这个分区称作 "(hd0,4)"。GRUB 对硬盘和分区的编号都是从 0 开始计算。另外，硬盘和分区都用逗号分隔，整个表达式用括号括起。现在，可以发现如果要引导 Linux 硬盘 hda5，应输入 "root (hd0,4)"。 

知道了内核在哪儿，还要具体指出哪个文件是内核文件，这就是kernel的工作。 
kernel /boot/vmlinuz-2.2.18 root=/dev/hda3 ro说明/boot/vmlinuz-2.2.18 就是要载入的内核。后面的都是传递给内核的参数。root=/dev/hda3就是linux的硬盘分区表示法，ro是以readonly的意思。 
initrd用来初始的linux image，并设置相应的参数。 

是不是感觉很简单啊！再来看一看windows的定义段吧。 
这里，我添加了一项来引导 Windows2000。要完成此操作，GRUB 使用了“链式装入器”(chainloader)。链式装入器从分区 (hd0,0) 的引导记录中装入 win2000 自己的引导装入器，然后引导它。这就是这种技术叫做链式装入的原因 -- 它创建了一个从引导装入器到另一个的链。这种链式装入技术可以用于引导任何版本的 DOS 或 Windows。 

我的RedHat linux在硬盘主引导分区装了lilo，所以也用了chainloader。 

GRUB的配置文件要简单就这么简单，如果你要更个性化一点，试一试把“color light-gray/blue ”加在default语句的下面，下一次启动GRUB时，看看有什么变化，再试一试“color light-blue/red",惊喜吗？ 有趣吧! 

###################### 
# GRUB的交互性 # 
###################### 




GRUB 最好的优点之一就是其强健的设计 -- 在不断使用它时请别忘了这点。如果更新内核或更改它在磁盘上的位置，不必重新安装 GRUB。事实上，如有必要，只要更新 menu.lst 文件即可，一切将保持正常。 

只有少数情况下，才需要将 GRUB 引导装入器重新安装到引导记录。首先，如果更改 GRUB root 分区的分区类型（例如，从 ext2 改成 ReiserFS），则需要重新安装。或者，如果更新 /boot/grub 中的 stage1 和 stage2 文件，由于它们来自更新版本的 GRUB，很有可能要重新安装引导装入器。其它情况下，可以不必理睬！ 

GRUB的最大的特点就是交互性特别强。在开机时，按一下“c”，将进入GRUB 控制台。显示如下： 

GRUB version 0.5.96.1 (640K lower / 3072K upper memory) 

[ Minimal BASH-like line editing is supported. For the first word, TAB 
lists possible command completions. Anywhere else TAB lists the possible 
completions of a device/filename. ] 

grub&gt; 

欢迎使用 GRUB 控制台。现在，再研究命令： 
我将通过GRUB 控制台绕过lilo来启动RedHat linux， 

grub&gt; root (h 

现在，按一次 Tab 键。如果系统中有多个硬盘，GRUB 将显示可能完成的列表，从 "hd0" 开始。如果只有一个硬盘，GRUB 将插入 "hd0,"。如果有多个硬盘，继续进行，在 ("hd2") 中输入名称并在名称后紧跟着输入逗号，但不要按 Enter 键。部分完成的 root 命令看起来如下： 

grub&gt; root (hd0, 

现在，继续操作，再按一次 Tab 键。GRUB 将显示特定硬盘上所有分区的列表，以及它们的文件系统类型。在我的系统中，按 Tab 键时得到以下列表： 

grub&gt; root (hd0, (tab，按tab一下键) 
Possible partitions are: 
Partition num: 0, Filesystem type is fat, partition type 0x6 
Partition num: 2, Filesystem type is ext2fs, partition type 0x83 
Partition num: 4, Filesystem type unknown, partition type 0x7 
Partition num: 5, Filesystem type is ext2fs, partition type 0x83 
Partition num: 6, Filesystem type is fat, partition type 0xb 
Partition num: 7, Filesystem type is fat, partition type 0xb 
Partition num: 8, Filesystem type is ext2fs, partition type 0x83 
Partition num: 9, Filesystem type unknown, partition type 0x82 

如您所见，GRUB 的交互式硬盘和分区名称实现功能非常有条理。这些，只需要好好理解 GRUB 新奇的硬盘和分区命名语法，然后就可以继续操作了 
grub&gt; root (hd0,8) 
现在已安装了 root 文件系统，到装入内核的时候了 

grub&gt; kernel /boot/vmlinuz-2.4.2 root=/dev/hda5 ro 
[Linux-bzImage, setup=0x1200, size=0xe1a30] 

您已经安装了 root 文件系统并装入了内核。现在，可以引导了。只要输入 "boot"，Linux 引导过程就将开始。是不是很cool啊，GRUB的menu.lst更像一个linux下的脚本程序。 


##################### 
# GRUB启动盘 # 
##################### 
要制作引导盘，需执行一些简单的步骤。首先，在新的软盘上创建 ext2 文件系统。然后，将其安装，并将一些 GRUB 文件复制到该文件系统，最后运行 "grub" 程序，它将负责设置软盘的引导扇区。准备好了吗？ 

将一张空盘插入 1.44MB 软驱，输入： 

# mke2fs /dev/fd0 
创建了 ext2 文件系统后，需要安装该文件系统： 

# mount /dev/fd0 /mnt/floppy 
现在，需要创建一些目录，并将一些关键文件（原先安装 GRUB 时已安装了这些文件）复制到软盘： 

# mkdir /mnt/floppy/boot 
# mkdir /mnt/floppy/boot/grub 
# cp /boot/grub/stage1 /mnt/floppy/boot/grub 
# cp /boot/grub/stage2 /mnt/floppy/boot/grub 
再有一个步骤，就能得到可用的引导盘。 

在linux bash中，从 root 用户运行“grub”，该程序非常有趣并值得注意，因为它实际上是 GRUB 引导装入器的半功能性版本。尽管 Linux 已经启动并正在运行，您仍可以运行 GRUB 并执行某些任务，而且其界面与使用 GRUB 引导盘或将 GRUB 安装到硬盘 MBR 时看到的界面(即GRUB控制台)完全相同。 
在 grub&gt; 提示符处，输入： 

grub&gt; root (fd0) 
grub&gt; setup (fd0) 
grub&gt; quit 

现在，引导盘完成了。 
如果要把GRUB装到硬盘上，也很容易。这个过程几乎与引导盘安装过程一样。首先，需要决定哪个硬盘分区将成为 root GRUB 分区。在这个分区上，创建 /boot/grub 目录，并将 stage1 和 stage2 文件复制到该目录中，可以通过重新引导系统并使用引导盘，或者使用驻留版本的 GRUB 来执行后一步操作。在这两种情况下，启动 GRUB，并用 root 命令指定 root 分区。例如，如果将 stage1 和 stage2 文件复制到 hda5 的 /boot/grub 目录中，应输入 "root (hd0,4)"。接着，决定在哪里安装 GRUB -- 在硬盘的 MBR，或者如果与 GRUB 一起使用另一个“主”引导装入器，则安装在特定分区的引导记录中。如果安装到 MBR，则可以指定整个磁盘而不必指定分区，如下（对于 hda）： 

grub&gt; setup (hd0) 

如果要将 GRUB 安装到 /dev/hda5 的引导记录中，应输入： 

grub&gt; setup (hd0,4) 

现在，已安装 GRUB。引导系统时，应该立即以 GRUB 的控制台方式结束（如果安装到 MBR）。现在，应创建引导菜单，这样就不必在每次引导系统时都输入那些命令。 



小结：在这里只是介绍了 GRUB 的一部分。例如，可以使用 GRUB 来执行网络引导，引导 BSD 文件系统，或更多操作。另外，GRUB 有许多配置和安全性命令也很有用。如需所有 GRUB 功能的完整描述，请阅读 GRUB 出色的 GNU 文档。只要在 bash 提示中输入 "info grub" 就可以阅读该文档。 


有用的一些信息：xosl是一个支持鼠标的图形界面boot loader，可以于system command和boot manager相比， 
网址是www.xosl.org。 

GRUB的下载：ftp://alpha.gnu.org/gnu/grub/ 


再补充：三种硬盘安装方法的 grub
命令集（采用任何一种都可以的，随便你喜欢哪个方法）：

1。用 hd.img 安装，这需要用到 grub for dos 的软盘仿真功能：

grub&gt; map (hd0,0)/hd.img (fd0)
grub&gt; chainloader (hd0,0)/hd.img
grub&gt; rootnoverify (fd0)
grub&gt; boot

2。用 vmlinuz 和 hd.rdz 两个文件来安装（无需使用 grub for dos，用 GNU 原来的
GRUB 都管用）：

grub&gt; kernel (hd0,0)/vmlinuz ramdisk_size=128000 root=/dev/ram3
automatic=method:disk acpi=ht vga=788
grub&gt; initrd (hd0,0)/hd.rdz
grub&gt; boot
注意 kernel 一行很长，不要截断成两行。还要注意上述命令都假定这些文件位于
(hd0,0) 的根目录，如果你的不同，当然要作适当的修改
来源：LinuxEden


3.首先下载grub for dos(http://grub.linuxeden.com),其最新版本支持ntfs分区，而且可以利用ntloader调用，比如winxp的引导菜单.
提取grldr到c：/下； 
修改boot.ini,加入 C:\GRLDR=Boot Grub （方法：在桌面我的电脑点右键－－属性－－高级－－启动和故障恢复－设置－－编辑，不用到c盘去找了，麻烦)； 
在c盘根目录下建立/boot/grub文件夹，建立menu.lst文本文件；
把ML的iso放在vfat分区，提取mbvmlinuz，mbinitrd-hd.gz与iso都放在根目录下 ；
修改menu.lst,加入 
代码: 

 title Magci linux1.2-setup 
      kernel (hd0,6)/mbvmlinuz ro root=/dev/ram0  ramdisk_size=32000 vga=788 
      initrd (hd0,6)/mbinitrd-hd.gz 

（hd0,6)为我的放置iso和mbvmlinuz，mbinitrd-hd.gz的分区，修改成你的 
注意kernel后有个空格 ；
重启，选择boot grub，选择Magic linux1.2-setup ；
后面的我就不说了，按照提示一步一步来就行了； 
当然你可以在安装成功后，修改menu.lst,加入你的ML启动项，你就可以用grub 
for dos 启动你的ML。 


################## ################## ################## ################## ################## ################## 
我的无光驱软驱，直接由iso文件安装mandriva的方法,(其它linux也同理)。
首先，需要把第一张cd中的install/alt1目录下的vmlinuz 和 all.rdz 解压出来。说明：这层目录下面还有alt0和alt2，它们安装了
不同的内核，详情可见install下面的说明文件，(文件名忘记了)。

其次，这种方法利用iso安装的原理基本上就是利用grub引导安装映象，那么我介绍我所知的三种方法：

A，已经拥有了grub引导，比如原有的linux仍存在，而且是由grub引导系统的。(这种情况比较简单)。
1,只要确定好上一步解压出来的vmlinuz 和 all.rdz在硬盘上的位置，比如第一块硬盘的第一个分区是/dev/hda1,那么改分区的位置在grub
中就表示为(hd0, 0);
2,然后就可以利用原来的grub引导系统，当出现grub引导菜单的时候，根据下面的提示，按 "c"，会出现命令行式的grub，然后按照一下格式
输入：(以第一步中的位置为例)
kernel (hd0,0)/vmlinuz ramdisk_size=128000 root=/dev/ram3 automatic=method:disk acpi=ht vga=788  ＃注释，然后输入回车
initrd (hd0,0)/all.rdz    ＃注释，然后输入回车
boot                      ＃注释，然后输入回车                                                                           

就可以看到引导安装开始了，方法A 结束。

B，如果没有grub，但是有装好的windows(以winxp为例)，也可以利用windows的c:盘下的boot.ini 结合 grub for dos引导安装。这里根据直接用winxp 引导 grub for dos，或者进入实dos再用grub for dos，可以分为一下两种情况。

B1, winxp 的boot.ini + grub_for_dos中的grldr;
在新版的grub_for_dos中，出现了一个文件grldr,它可以直接由winxp引导，实现引导grub，这样就不用安装grub了。方法如下：
1, 把grub_for_dos中的grldr 和 boot目录拷贝到c盘，就是和boot.ini所在的分区的根目录下；
2，编辑boot.ini,在最后加上一行，
C:\GRLDR="grub for dos"
3, 编辑boot/grub/menu.lst,如下:
title mandriva install
kernel (hd0,0)/vmlinuz ramdisk_size=128000 root=/dev/ram3 automatic=method:disk acpi=ht vga=788
initrd (hd0,0)/all.rdz
注意，为了方便，也可以直接把menu.lst放在grldr所在的分区根目录。
4, 重启，然后在winxp的引导菜单选grub for dos就可以引导安装了。

B2， winxp的boot.ini + vfloppy + grub_for_dos
1,这种方法是首先在winxp中安装vfloppy，方法就不介绍了，这样在winxp引导菜单中选vfloppy对应的项，就可以进入实dos中了;
2,在dos中运行grub_for_dos中的grub.exe，可以直接指定由B1中编辑好的menu.lst,这样比较方便：
grub --config-file=(hd0,0)/boot/grub/menu.lst ，运行就可以引导安装了。


对于方法A和B，当引导安装开始后，只要指定系统安装所需的iso文件所需的位置就可以了。

以上方法所需要的软件，可以在这里下载，http://lsec.cc.ac.cn/~peace/service/software/win4linux.rar ，当然也可以在网上下载更新
的版本。

再补充 不用grub，直接用u盘引导从硬盘安装linux的方法。
1),这里利用mandriva提供的all.img，一般来说，解压cd1，在cd1/install/image/all.img;
2),插上U盘，搞清楚U盘的设备号，用mount命令即可，我这里是/dev/sda1;
3),用root，执行 dd if=path/all.img of=/dev/sda1即可；
4),用u盘引导，进入图形化安装过程，输入iso文件所在的位置即可。




