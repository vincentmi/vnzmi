---
layout:     post
title:      "外置采集温度_让arduino用2颗5号电池运行1年以上 "
date:       2015-05-08 14:16:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - HW
    - Arduino
---

文章来自极客工坊，因此加密了只自己能看纯收藏
[http://www.geek-workshop.com/thread-12261-1-1.html](http://www.geek-workshop.com/thread-12261-1-1.html)
作者：mylife1213

这次讲功耗.

如果你想把arduino avr类的开发项目用来便携式设置上,不管商业还是个人DIY,那么你头一个要对付的问题就是设备功耗!

我测试atmega328p(大部分arduino 都是基于这个处理器) 最小系统下(16Mhz)运行功耗是10ma,那么如果不对处理器进行任何节电处理的话一块手机1500mah的电池只能不间断运行  1500/10/24=6.5天 ,这个还是在没有任何外围元器件的情况下的运行时间! 


<!--more-->


现在物联网非常火,那么物联网正常情况是需要多个节点进行数据采集,然后上报给主机进行联网操作,或者接收主机命令进行对其他电器的操作. 那个问题就出现了,很多时候数据采集的地方是没有电源的,比如外置气象数据采集,这个时候就需要采集设备可以使用电池来驱动,而且不能频繁的更换电池!这就需要用到处理器的节电方案!
    
下面我将介绍ATMEGA328P的节电解决方案.

328P有8种节电设置,分别是:

**空闲模式**
当SM2..0 为000 时， SLEEP 指令将使MCU 进入空闲模式。在此模式下，CPU 停止运
行，而SPI、USART、模拟比较器、ADC、两线串行接口、定时器/ 计数器、看门狗和
中断系统继续工作。这个睡眠模式只停止了clkCPU 和clkFLASH，其他时钟则继续工作。
象定时器溢出与USART 传输完成等内外部中断都可以唤醒MCU。如果不需要从模拟比
较器中断唤醒MCU，为了减少功耗，可以切断比较器的电源。方法是置位模拟比较器控
制和状态寄存器ACSR 的ACD。如果ADC 使能，进入此模式后将自动启动一次转换。


**ADC 噪声抑制模式**
当SM2..0 为001 时， SLEEP 指令将使MCU 进入噪声抑制模式。在此模式下，CPU 停
止运行，而ADC、外部中断、两线接口地址配置、定时器/ 计数器2 和看门狗继续工作。
这个睡眠模式只停止了clkI/O、clkCPU 和clkFLASH，其他时钟则继续工作。
此模式提高了ADC 的噪声环境，使得转换精度更高。ADC 使能的时候，进入此模式将
自动启动一次AD 转换。ADC 转换结束中断、外部复位、看门狗复位、BOD 复位、两线
接口地址匹配中断、定时器/ 计数器2 中断、SPM/EEPROM 准备好中断、外部电平中断
INT0 或INT1，或外部中断INT2 可以将MCU 从ADC 噪声抑制模式唤醒。


**掉电模式**
当SM2..0 为010 时， SLEEP 指令将使MCU 进入掉电模式。在此模式下，外部晶体停
振，而外部中断、两线接口地址匹配及看门狗（如果使能的话）继续工作。只有外部复
位、看门狗复位、BOD 复位、两线接口地址匹配中断、外部电平中断INT0 或INT1，或
外部中断INT2 可以使MCU 脱离掉电模式。这个睡眠模式停止了所有的时钟，只有异步
模块可以继续工作。


**省电模式**
当SM2..0 为011 时， SLEEP 指令将使MCU 进入省电模式。这一模式与掉电模式只有
一点不同：
如果定时器/ 计数器2 为异步驱动，即寄存器ASSR 的AS2 置位，则定时器/ 计数器2 在
睡眠时继续运行。除了掉电模式的唤醒方式，定时器/ 计数器2 的溢出中断和比较匹配中
断也可以将MCU 从休眠方式唤醒，只要TIMSK 使能了这些中断，而且SREG 的全局中
断使能位I 置位。
如果异步定时器不是异步驱动的，建议使用掉电模式，而不是省电模式。因为在省电模式
下，若AS2 为0，则MCU 唤醒后异步定时器的寄存器数值是没有定义的。
这个睡眠模式停止了除clkASY 以外所有的时钟，只有异步模块可以继续工作。



**Standby 模式**
当SM2..0 为110 时， SLEEP 指令将使MCU 进入Standby 模式。这一模式与掉电模式唯一的不同之处在于振荡器继续工作。其唤醒时间只需要6 个时钟周期。

**扩展Standby 模式**
当SM2..0 为111 时， SLEEP 指令将使MCU 进入扩展的Standby 模式。这一模式与省掉电模式唯一的不同之处在于振荡器继续工作。其唤醒时间只需要6 个时钟周期。




下图是各个模式下关闭的模块

![184547gceyoeqota2y277m.png][/img/in-post/3108120046.png]

那么我们正常使用的是掉电模式,在掉电模式下328p测试耗电1ua,这是什么概念,2颗5号电池在处理器没有进行其他操作的情况下可以工作79年!
当然了,我们不可能让处理器就这样一直待机不做其他事情,我们需要定期唤醒328P,让他处理事情,比如采集温湿度,PM2.5数据发送给主机.那么如何唤醒呢? 答案是在掉电模式下你只能通过外部中断和看门狗来唤醒328P,外部中断唤醒需要外围电路,我们优先选择WDT看门狗进行唤醒.这里的看门狗不是你们知道的只有重启328P的功能!他也可以配置成中断事件! " ISR(WDT_vect) "中断函数,通过看门狗我们就可以在不添加外围元件的情况设置唤醒时间了!

下面看实例:
```c
#include <avr/sleep.h>
#include <avr/wdt.h>
 
volatile byte data=0;
 
void setup() {
  pinMode(13,OUTPUT);
  setup_watchdog(9);
// 0=16ms, 1=32ms,2=64ms,3=128ms,4=250ms,5=500ms
// 6=1 sec,7=2 sec, 8=4 sec, 9= 8sec
  ACSR |=_BV(ACD);//OFF ACD
  ADCSRA=0;//OFF ADC
  Sleep_avr();//Sleep_Mode
}
 
void loop() {
 
 if(data>=7){
  data=0;
//-------------------------------
   digitalWrite(13,HIGH);
  delay(100);                      //此处是到达设置唤醒时间允许的程序
  digitalWrite(13,LOW); 
//--------------------------------    
Sleep_avr();
 }
 else {
  Sleep_avr();  //Continue Sleep
 }
 
}
 
//Sleep mode is activated
void setup_watchdog(int ii) {
 
  byte bb;
 
  if (ii > 9 ) ii=9;
  bb=ii & 7;
  if (ii > 7) bb|= (1<<5);
  bb|= (1<<WDCE);
 
  MCUSR &= ~(1<<WDRF);
  // start timed sequence
  WDTCSR |= (1<<WDCE) | (1<<WDE);
  // set new watchdog timeout value
  WDTCSR = bb;
  WDTCSR |= _BV(WDIE);
 
 
}
//WDT interrupt
ISR(WDT_vect) {
 
  ++data;
 // wdt_reset();
 
}
 
void Sleep_avr(){
  set_sleep_mode(SLEEP_MODE_PWR_DOWN  ); // sleep mode is set here
  sleep_enable();
  sleep_mode();                        // System sleeps here
}
```

这是一个配置成56秒唤醒一次对5号端口设置高电平100ms的程序,其中if(data>=7)是data(看门狗)超时大于7次就唤醒CPU进行高电平100ms的函数,看门狗超时时间已设置成8秒,你可以调节if(data>=7)设置成你想要的唤醒时间!
通过这样的节电设置以后这个程序可以运行至少几年!

代码用arduino IDE写的,IDE不支持中文注释,英文注释将就看吧,不理解的代码留言解答.

要改变唤醒时间是改这个函数:
if(data>=7) 
函数里面7的意思是有7次看门狗8秒超时复位.比如你要设置24秒那就写if(data>=3)
公式是:3*8=24


使用休眠模式制作了一个外置气象站，使用amtega328P用nrf24l01发送ds18b20采集的数据，每2分钟发生一次，平时待机功耗控制在10ua左右，设计可以使用2颗南孚电池工作超过1年时间

实物图

![211541geoqq8wodddzdqhw.png](/img/in-post/338645405.png)


外置发送硬件先按照328P最小系统搭建，然后连接nrf24l01p与ds1820b.


按照arduino 引脚连接如下表
```
arduino     nrf24l01p
13->         SCK
12->         MISO     
11->         MOSI
8->           CE
7->           CSN
arduino     ds1820b
4->            数据引脚，其他连接GND  VCC
```

室内接收机可以使用pro mini 和uno

接线方式如下：
```
arduino     nrf24l01p

13->         SCK
12->         MISO     
11->         MOSI
9->          CE
8->         CSN

2->         IRQ
注意nrf24l01电源要接3.3v
```
提供代码下载
[nrf24l01P.rar](/img/in-post/931264314.rar)

read_WDT是接收机
WDT_2是室外机
