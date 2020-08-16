---
layout:     post
title:      "HTTP Client"
date:       2005-10-13 14:56:38
author:     "Vincent"
header-img:  "img/bullseye-gradient_blue.svg"
catalog: false
tags:
    - 新浪博客
    - 技术文章
---

## 代码

```java
import java.net.*;
import java.io.*;
import java.util.Properties;
import java.util.Enumeration;
public class  Http{
    protected Socket client;
    protected BufferedOutputStream sender;
    protected BufferedInputStream receiver;
    protected ByteArrayInputStream byteStream;
    protected URL target;
    private int responseCode=-1;
    private String responseMessage="";
    private String serverVersion="";
    private Properties header=new Properties();
    public Http(){}
    
    public Http(String url){
        GET(url);
        }
    /*GET方法根据URL，会请求文件、数据库查询结果、程序运行结果等多种内容*/
    
    public void GET(String url){
        try{
            checkHTTP(url);
            openServer(target.getHost(),target.getPort());
            String cmd="GET "+getURLFormat(target)+" HTTP/1.0\r\n"+getBaseHeads()+"\r\n";
            System.out.println(cmd);
            sendMessage(cmd);
            receiveMessage();
        }catch(ProtocolException p){
            p.printStackTrace();
            return;
        }catch(UnknownHostException e){
            e.printStackTrace();
            return;
        }catch(IOException i){
            i.printStackTrace();
            return;
        }
}
/*
*HEAD方法只请求URL的元信息，不包括URL本身。若怀疑本机和服务器上的
*文件相同，用这个方法检查最快捷有效。
*/
public void HEAD(String url){
    try{
        checkHTTP(url);
        openServer(target.getHost(),target.getPort());
        String cmd="HEAD "+getURLFormat(target)+" HTTP/1.0\r\n"+getBaseHeads()+"\r\n";
        System.out.println(cmd);
        sendMessage(cmd);
        receiveMessage();
    }catch(ProtocolException p){
        p.printStackTrace();
        return;
    }catch(UnknownHostException e){
        e.printStackTrace();
        return;
    }catch(IOException i){
        i.printStackTrace();
        return;
    }
}
/*
*POST方法是向服务器传送数据，以便服务器做出相应的处理。例如网页上常用的
*提交表格。
*/
public void POST(String url,String content){
    try{
        checkHTTP(url);
        openServer(target.getHost(),target.getPort());
        String cmd="POST "+getURLFormat(target)+" HTTP/1.0\r\n"+getBaseHeads();
        cmd+="Content-type:application/x-www-form-urlencoded\r\n";
        cmd+="Content-length:"+content.length()+"\r\n\r\n";
        cmd+=content+"\r\n";
  System.out.println(cmd);
        sendMessage(cmd);
        receiveMessage();
    }catch(ProtocolException p){
        p.printStackTrace();
        return;
    }catch(UnknownHostException e){
            e.printStackTrace();
            return;
    }catch(IOException i){
        i.printStackTrace();
        return;
    }
}
protected void checkHTTP(String url)throws ProtocolException{
    try{
        URL target=new URL(url);
        if(target==null||!target.getProtocol().toUpperCase().equals("HTTP"))
        throw new ProtocolException("这不是HTTP协议");
        this.target=target;
    }catch(MalformedURLException m){
        throw new ProtocolException("协议格式错误");
    }
}
/*
*与Web服务器连接。若找不到Web服务器，InetAddress会引发UnknownHostException
*异常。若Socket连接失败，会引发IOException异常。
*/
protected void openServer(String host,int port)throws UnknownHostException,IOException{
    header.clear();
    responseMessage="";responseCode=-1;
    try{
        if(client!=null)closeServer();
        if(byteStream!=null){
            byteStream.close();byteStream=null;
        }
        InetAddress address=InetAddress.getByName(host);
        client=new Socket(address,port==-1?80:port);
        sender=new BufferedOutputStream(client.getOutputStream());
        receiver=new BufferedInputStream(client.getInputStream());
    }catch(UnknownHostException u){
        throw u;
    }catch(IOException i){
        throw i;
    }
}
/*关闭与Web服务器的连接*/
protected void closeServer()throws IOException{
    if(client==null)return;
    try{
        client.close();
        sender.close();
        receiver.close();
    }catch(IOException i){
        throw i;
    }
    
    client=null;sender=null;receiver=null;
    }
    
protected String getURLFormat(URL target){
    
        String spec="http://"+target.getHost();
        if(target.getPort()!=-1)spec+=":"+target.getPort();
        return spec+=target.getFile();
}
/*向Web服务器传送数据*/
protected void sendMessage(String data)throws IOException{
    System.out.println(data);
    sender.write(data.getBytes(),0,data.length());
    sender.flush();
}
/*接收来自Web服务器的数据*/
protected void receiveMessage()throws IOException{
    byte data[]=new byte[1024];
    int count=0;
    int word=-1;
    //解析第一行
    while((word=receiver.read(data))!=-1){
        System.out.print(new String(data));
    }
    closeServer();      
}
public String getResponseMessage(){
    return responseMessage;
}
public int getResponseCode(){
    return responseCode;
}
public String getServerVersion(){
    return serverVersion;
}
public InputStream getInputStream(){
    return byteStream;
}
public synchronized String getHeaderKey(int i){
    if(i&gt;=header.size())return null;
    Enumeration enum1=header.propertyNames();
    String key=null;
    for(int j=0;j&lt;=i;j++)
        key=(String)enum1.nextElement();
    return key;
}
public synchronized String getHeaderValue(int i){
    if(i&gt;=header.size())return null;
    return header.getProperty(getHeaderKey(i));
}
public synchronized String getHeaderValue(String key){
    return header.getProperty(key);
}
protected String getBaseHeads(){
    String inf="User-Agent:myselfHttp/1.0\r\n"+"Accept:www/source;text/html;image/gif;*/*\r\n";
    return inf;
}
private byte[] addCapacity(byte rece[]){
    byte temp[]=new byte[rece.length+1024];
    System.arraycopy(rece,0,temp,0,rece.length);
    return temp;
}
public static void main(String[]args){
    Http http=new Http();
    //http.GET("http://192.168.1.5");
    //http.HEAD("http://www.xdol.com.cn/");
    int i;
 http.POST("http://www.7rings.com.cn/crbt/login.php","userid=89919419&amp;passwd=020752&amp;areacode=00&amp;phone_type=0");
 //Thread.sleep(5000);
    //http.GET("http://localhost/WEB_ROOT/admin/broadcaster.php");
    for(i=0;i&lt;10;i++){
        
        //http.POST("http://www.model-dl.com/modelinfo.asp?modelid=101","ratecontd=101&amp;MM_insert=form1");
        }
    }
}
```
 

## HTTP请求

 
```
 ----------运行这个java程序并捕获输出 ----------
POST http://www.7rings.com.cn/crbt/login.php HTTP/1.0
User-Agent:myself
Http/1.0
Accept:www/source;text/html;image/gif;*/*Content-type:application/x-www-form-urlencodedContent-length:54

userid=89919419&amp;passwd=******&amp;areacode=00&amp;phone_type=0
```
 

## 响应内容

 
```
HTTP/1.1 200 OK
Date: Thu, 13 Oct 2005 06:45:03 GMT
Server: Apache/1.3.33 (Unix) PHP/5.0.3
X-Powered-By: PHP/5.0.3
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Last-Modified: Thu, 13 Oct 2005 06:45:03
GMTCache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cacheSet-Cookie: PHPSESSID=in2k6uuso7ffjkul00n480f1i2; path=/Set-Cookie: crbt_area_code=00; expires=Sat, 12-Nov-2005 06:45:03 GMT; path=/; domain=www.7rings.com.cnConnection: closeContent-Type: text/html; charset=gb2312

<script><document.frames.top.location='index02.php?url=myringlist.php'</script>
```                             



