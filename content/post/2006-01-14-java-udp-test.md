---
layout:     post
title:      "Java UDP 简单程序"
date:       2006-01-14 12:22:49
author:     "Vincent"
image:  "img/bullseye-gradient_blue.svg"
catalog: true
tags:
    - 新浪博客
    - 技术文章
---



# Server

```java
/* * Miwenshu Created on 2005-9-15 * */
import java.net.*;
import java.io.*;
class DatagramServer{
    private static int PORT=8122;
    public static void main(String[] args) {
        try{
            System.out.println("Datagram Server.");
            byte[] buf = new byte[1000];
            DatagramSocket ds = new DatagramSocket(PORT); 
            //开始监视12345端口
            DatagramPacket ip = new DatagramPacket(buf, buf.length);
             //创建接收数据报的实例  
             int i=0;
             String base="";
             while (true) {
                ds.receive(ip); //阻塞，直到收到数据报后将数据装入IP中   
                String info=new String(buf);
                if(i==1) 
                    base=info;   
                if(base.equals(info)){

                }else{
                    System.out.println("-------------");
                    System.out.println(info.trim()); 
                    base=info;   
                }
                i++;
            }
        }catch(SocketException e1){
            System.out.println("SocketException");
        }catch( UnknownHostException e11){
            System.out.println("UnknownHostException");
        }catch(IOException e){
            System.out.println("IOException");
        }
    }
}
```

## Client

```java
import java.net.*;
import java.util.Enumeration;
import java.io.*;
class  DatagramClient{
    private static int PORT=8122;//listen.....
    private static int SENDPORT=9999;//listen....
    public static void main(String[] args) {
        try{
            System.out.println("UDP CLient Start!");
            //{发送数据的客户端}
            byte[] ip={(byte)192,(byte)168,(byte)1,(byte)7};
            NetworkInterface tmp_ni=null;
            InetAddress tmp_ia=null;
            Enumeration ni=NetworkInterface.getNetworkInterfaces();
            String info="";
            while(ni.hasMoreElements()){
                tmp_ni=(NetworkInterface)ni.nextElement();
                String dispName=new String(tmp_ni.getDisplayName().getBytes(),"GB2312");
                info+="Interface("+tmp_ni.getName()+"):"+dispName+"\n";
                Enumeration ia=tmp_ni.getInetAddresses();
                while(ia.hasMoreElements()){
                    tmp_ia=(InetAddress)ia.nextElement();
                    info+="\t ip:"+tmp_ia.getHostAddress()+"\n";
                }
            }
            ///////////////////////////////////////////////
            InetAddress target = InetAddress.getByAddress(ip); 
            System.out.println("Sent to :"+target.getHostAddress()+":"+PORT);
            //得到目标机器的地址实例
            DatagramSocket ds = new DatagramSocket(SENDPORT); 
            //从9999端口发送数据报
            InetAddress local=InetAddress.getLocalHost();
            String hello = info;
            //要发送的数据
            byte[] buf=hello.getBytes();
            //将数据转换成Byte类型
            DatagramPacket op = new DatagramPacket(buf, buf.length, target, PORT); 
            //将BUF缓冲区中的数据打包
            while(true){
                ds.send(op);
                System.out.println(info);
                Thread.sleep(1000);
            }
            //发送数据
            //
            ds.close();
            //关闭连接
        }catch(SocketException e1){
            System.out.println("SocketException");
        }catch( UnknownHostException e11){
            System.out.println("UnknownHostException");
        }catch(IOException e){ 
            System.out.println("IOException");
        }catch(InterruptedException e1111){
            System.out.println("InterruptedException");
        }
    }
}//向服务器报告IP
```



