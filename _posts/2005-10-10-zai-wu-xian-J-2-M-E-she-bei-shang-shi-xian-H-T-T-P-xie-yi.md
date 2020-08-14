---
layout:     post
title:      "在无线J2ME设备上实现HTTP协议　"
date:       2005-10-10 22:50:36
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: true
tags:
    - 新浪博客
    - 技术文章
---


随着越来越多手提电话和个人数字助理开始融入到信息高速公路之上，从移动设备上访问Web站点变得越来越重要。Java开创了消费设备中小型的储存容量的先河，它是用于开发手机、传呼机及其他微型设备应用程序的理想语言。　　在本文中，我们将学习如何从一个J2ME客户机上向服务器发送一条HTTPGET请求和一条HTTPPOST请求。虽然这只是一篇探讨性质的文章，但是我还是假定读者已经熟悉Java，J2ME，以及JavaMidlets（MIDP应用程序）的运作机制。我们将使用J2ME的MIDP简表，并利用SUN的J2ME的无线应用程序开发工具包编译、配置和测试我们的应用程序。对于HTTP服务器，任何WWW地址都可以被访问，但是默认时我们将使用一个简单的JavaServlet来返回我们的HTTP请求的细节。

　　如何使用J2ME客户机向Web服务器和类似的支持HTTP的服务器发送HTTP请求呢？答案就是使用可在javax.microedition.io程序包中可找到的J2ME的网络类。本文就想具体阐述这个问题。

　　本文概述∶　　使用J2ME设计无线网络应用程序　　.发送一条超文本GET请求　　.发送一条超文本POST请求　　.使用J2ME进行无线网络编程

　　Java的网络编程能力是相当健壮的。Java2标准版(J2SE)在java.io和java.net程序包中定义了100多个接口程序，类和异常。通过这些库实现的功能是很强大的，但是这只适用于传统的计算机系统，这些计算机系统有强大的CPU处理能力，快速的内存和持久的数据储存，但是这些在大多数的无线设备上是不现实的。因此，J2ME定义了这些函数的子集，并提供了一套用于网络和文件访问的固定的程序包---javax.microedition.io程序包。由于可移动设备种类繁多，这个程序包仅仅定义了一套接口，而为每个可移动设备供应厂商留下了实际的应用程序接口实现。这就在可移植性和设备特定特征的应用中找到了一个最佳的平衡点。

　　定义在javax.microedition.io类中的抽象网络和文件输入输出框架称为通用连接框架（GenericConnectionFramework，简称GCF）。GCF定义了一套有关抽象化的内容来描述不同的通信方法。最高级的抽象被称作连接（Connection），还声明了六个接口（四个是直接的，两个是间接的）。这七个接口就构成了J2ME的CLDC的一部分，CLDC是大多数的能使用Java的无线设备使用的配置。设计这个配置的目的就是为所有的CLDC设备（手提电话，双向传呼机，低档的PDA等等)提供公用的网络和文件输入输出能力。虽然GCF的目的是公用网络和文件输入输出框架，但是生产商并不要求实现GCF中声明的所有的接口。有的厂家可以决定只支持socket连接，而其它的厂家可以选择只支持基于数据报的通信。为了促进跨越类似装置的可移植性，MIDP规范要求所有的MIDP设备实现HttpConnection接口。HttpConnection不是GCF的一部分，但是它是从GCF的一个接口ContentConnection衍生出来的。我们将使用HttpConnection接口构造我们样本应用程序。

发送一个HTTPGET请求

　　这一节将重点解释程序代码，在下一节中我们将只讲述被用来发送HTTP请求并检索由服务器返回的响应通用连接框架接口和HttpConnection接口。创建MIDP用户界面的程序代码见附录。

　　我们先要定义一个方法来放用于发送HTTPGET请求的代码。因为这个方法中的有些操作有潜在的抛出IOException的可能，所以我们将把这样的意外(exception)抛给调用方法。

publicStringsendHttpGet(Stringurl)throwsIOException{;HttpConnectionhcon=null;DataInputStreamdis=null;StringBuffermessage="";try{;

　　第一步是使用Connector类打开一个到服务器的连接，这是GCF的关键。我们将把这个连接强制转换为需要的类型，在本例中为HttpConnection类型。

hcon=(HttpConnection)Connector.open(url);

　　接下来，我们得到HttpConnection上的一个DataInputStream，允许我们一个字符一个字符的读取服务器的响应数据。

dis=newDataInputStream(hcon.openInputStream());

　　使用DataInputStream的read()方法，服务器响应的每个字符都被集中起来放入StringBuffer对象。

intch;while((ch=dis.read())!=-1){;message=message.append((char)ch);};

　　最后，连接对象被净空以保存资源，而信息从这个方法中返回。

};finally{;if(hcon!=null)hcon.close();if(dis!=null)dis.close();};//结束try/finally代码段returnmessage.toString();};//结束sendGetRequest(String)

　　如何发送一个HTTPPOST请求

　　你可以想象，发送一个HTTPPOST请求的处理过程其实与发送一个GET请求非常地类似。我们将修改一个现有命令，添加少量的新的命令，并添加一个来自通用连接框架的附加的对象和一个附加的StringBuffer对象把POST请求体重的内容发送到服务器中。剩下的命令将保持不变。

　　复制我们刚才创建的sendHttpGet()方法，把它粘贴进同一个类文件，改名为sendHttpPost()。现在，我们将修改这个新方法来发送一个HTTPPOST请求到服务器。在方法的顶部添加两个新的变量说明。声明一个类型为DataOutputStream的变量和另一个String类型的变量。我们将使用DataOutputStream对象把存在于字符串变量中的POST请求体发送到服务器中。

DataOutputStreamdos=null;StringrequestBody=null;

　　修改connector.open()命令包含另一个参数，指出连接将允许客户端可以通过连接在服务器上读和写。

hcon=(HttpConnection)Connector.open(url,Connector.READ_WRITE);

　　设置HttpConnection对象使用的请求方法为POST（默认的方法是GET）。

hcon.setRequestMethod(HttpConnection.POST);

　　得到一个用于现有的HTTP连接的DataOutputStream对象。

dos=hc.openDataOutputStream();

　　声明一个字节数组并通过检索一个来自requestBody字符串的字节数组初始化。然后把DataOutputStream的缓冲写入字节数组内。

byte[]byteRequest=requestBody.getBytes();for(inti=0;i&lt;byteRequest.length;i++){;dos.writeByte(byteRequest[i]);};//结束for(inti=0;i&lt;byteRequest.length;i++)

dos.flush();//包含本句，在某些设被上将可能会产生不可预期的结果

　　调用flush()方法的意图是发送已经写入的数据到DataOutputStream的服务器的缓冲区中。在某些电话上，这个操作工作正常，在其他的电话上，它导致HTTP请求的Transfer-Encoding被设置为"chunked"，有一些随机字符被放到请求本身的前面和后面。那又怎样处理这个问题呢？这个方法调用实际上是根本不需要的。在接下来的一行中，服务器连接打开（通过openInputStream()），将自动输入缓冲区。因此，你最好不要调用缓冲区的flush()方法。这个方法其余的部分保持不变，除了DataOutputStream对象必须在finally{;};语句块中关闭。

};finally{;if(hc!=null)hc.close();

if(dis!=null)dis.close();

if(dos!=null)dis.close();};//结束try/finally

　　这就是所有的程序代码!并请参见本文后附带的程序代码。

　　随着可以使用国际互联网络和支持网络的无线设备日益的增多普及，Java和J2ME的重要性也在不断的变大。因为HTTP协议是当前仅有的，被所有的遵从MIDP规范的设备支持的网络协议，它也是用于开发无线网络应用程序的最好的候选者。

　　在本文中，我们探究了无线网络编程的基本结构和几个核心问题，我们看了如何调用两个最常用的HTTP请求方法：GET和POST。J2ME仍然在它的发展初期，并且无线设备也即将得到大面积的普及。所以，所有有志投身于无线网络编程中的开发者们将得到大展拳脚的好机会。

　　附录：

/**HttpMidlet.java*/importjavax.microedition.midlet.*;importjavax.microedition.lcdui.*;importjavax.microedition.io.*;importjava.io.*;

publicclassHttpMidletextendsMIDletimplementsCommandListener{;//使用默认的URL。用户可以从图形用户接口改变这个值privatestaticStringdefaultURL="http://localhost:8080/test/servlet/EchoServlet";;

//主MIDP显示privateDisplaymyDisplay=null;

//输入URL的图形用户接口组件privateformrequestScreen;privateTextFieldrequestField;

//用于提交请求的图形用户接口组件privateListlist;privateString[]menuItems;

//用于显示服务器响应的图形用户接口组件privateformresultScreen;privateStringItemresultField;

//用于requestScreen的"send"按钮CommandsendCommand;//用于requestScreen的"exit"按钮CommandexitCommand;//用于requestScreen的"back"按钮CommandbackCommand;

publicHttpMidlet(){;//初始化图形用户接口组件myDisplay=Display.getDisplay(this);sendCommand=newCommand("SEND",Command.OK,1);exitCommand=newCommand("EXIT",Command.OK,1);backCommand=newCommand("BACK",Command.OK,1);

//显示请求的URLrequestScreen=newform("TypeinaURL:");requestField=newTextField(null,defaultURL,100,TextField.URL);requestScreen.append(requestField);requestScreen.addCommand(sendCommand);requestScreen.addCommand(exitCommand);requestScreen.setCommandListener(this);

//选择想要的HTTP请求方法menuItems=newString[]{;"GETRequest","POSTRequest"};;list=newList("SelectanHTTPmethod:",List.IMPLICIT,menuItems,null);list.setCommandListener(this);

//先是从服务器上收到的信息resultScreen=newform("ServerResponse:");resultScreen.addCommand(backCommand);resultScreen.setCommandListener(this);

};//结束HttpMidlet()

publicvoidstartApp(){;myDisplay.setCurrent(requestScreen);};//结束startApp()

publicvoidcommandAction(Commandcom,Displayabledisp){;//当用户点击"send"按钮if(com==sendCommand){;myDisplay.setCurrent(list);};elseif(com==backCommand){;requestField.setString(defaultURL);myDisplay.setCurrent(requestScreen);};elseif(com==exitCommand){;destroyApp(true);notifyDestroyed();};//结束if(com==sendCommand)

if(disp==list&amp;&amp;com==List.SELECT_COMMAND){;

Stringresult;

if(list.getSelectedIndex()==0)//发送一个GET请求到服务器result=sendHttpGet(requestField.getString());else//发送一个POST请求到服务器result=sendHttpPost(requestField.getString());

resultField=newStringItem(null,result);resultScreen.append(resultField);myDisplay.setCurrent(resultScreen);};//结束if(dis==list&amp;&amp;com==List.SELECT_COMMAND)};//结束commandAction(Command,Displayable)

privateStringsendHttpGet(Stringurl){;HttpConnectionhcon=null;DataInputStreamdis=null;StringBufferresponseMessage=newStringBuffer();

try{;//使用READ权限的标准的HttpConnectionhcon=(HttpConnection)Connector.open(url);

//从HttpConnection取得一个DataInputStreamdis=newDataInputStream(hcon.openInputStream());

//从服务器上取回响应intch;while((ch=dis.read())!=-1){;responseMessage.append((char)ch);};//结束while((ch=dis.read())!=-1)};catch(Exceptione){;e.printStackTrace();responseMessage.append("ERROR");};finally{;try{;if(hcon!=null)hcon.close();if(dis!=null)dis.close();};catch(IOExceptionioe){;ioe.printStackTrace();};//结束try/catch};//结束try/catch/finallyreturnresponseMessage.toString();};//结束sendHttpGet(String)

privateStringsendHttpPost(Stringurl){;HttpConnectionhcon=null;DataInputStreamdis=null;DataOutputStreamdos=null;StringBufferresponseMessage=newStringBuffer();//请求体Stringrequeststring="ThisisaPOST.";

try{;//使用读写权限的HttpConnectionhcon=(HttpConnection)Connector.open(url,Connector.READ_WRITE);

//设置请求方法为POSThcon.setRequestMethod(HttpConnection.POST);

//取得发送请求字符串的DataOutputStreamdos=hcon.openDataOutputStream();byte[]request_body=requeststring.getBytes();

//发送请求字符串到服务器for(inti=0;i&lt;request_body.length;i++){;dos.writeByte(request_body[i]);};//结束for(inti=0;i&lt;request_body.length;i++)

//取得做为接收服务器响应的DataInputStreamdis=newDataInputStream(hcon.openInputStream());

//从服务器上取回响应intch;while((ch=dis.read())!=-1){;responseMessage.append((char)ch);};//结束while((ch=dis.read())!=-1){;};catch(Exceptione){;e.printStackTrace();responseMessage.append("ERROR");};finally{;//释放输入输出流和HTTP连接try{;if(hcon!=null)hcon.close();if(dis!=null)dis.close();if(dos!=null)dos.close();};catch(IOExceptionioe){;ioe.printStackTrace();};//结束try/catch};//结束try/catch/finallyreturnresponseMessage.toString();};//结束sendHttpPost(String)

publicvoidpauseApp(){;};//结束pauseApp()

publicvoiddestroyApp(booleanunconditional){;myDisplay=null;requestScreen=null;requestField=null;resultScreen=null;resultField=null;};//结束destroyApp(boolean)};//结束HttpMidlet



