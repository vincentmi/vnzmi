---
layout:     post
title:      "用JAVA中的动态代理实现数据库连接池"
date:       2006-01-14 12:25:17
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: false
tags:
    - 新浪博客
    - 技术文章
---



     内容：  参考资料   关于作者  对本文的评价    订阅:  developerWorks 时事通讯       刘冬珠海市创我科技发展有限公司软件工程师2002 年 12 月 05 日
作者通过使用JAVA中的动态代理实现数据库连接池，使使用者可以以普通的jdbc连接的使用习惯来使用连接池。数据库连接池在编写应用服务是经常需要用到的模块，太过频繁的连接数据库对服务性能来讲是一个瓶颈，使用缓冲池技术可以来消除这个瓶颈。我们可以在互联网上找到很多关于数据库连接池的源程序，但是都发现这样一个共同的问题：这些连接池的实现方法都不同程度地增加了与使用者之间的耦合度。很多的连接池都要求用户通过其规定的方法获取数据库的连接，这一点我们可以理解，毕竟目前所有的应用服务器取数据库连接的方式都是这种方式实现的。但是另外一个共同的问题是，它们同时不允许使用者显式的调用Connection.close()方法，而需要用其规定的一个方法来关闭连接。这种做法有两个缺点：
第一：改变了用户使用习惯，增加了用户的使用难度。
首先我们来看看一个正常的数据库操作过程：
int executeSQL(String sql) throws SQLException{ Connection conn = getConnection(); //通过某种方式获取数据库连接 PreparedStatement ps = null; int res = 0; try{  ps = conn.prepareStatement(sql);  res = ps.executeUpdate();}finally{try{ps.close();}catch(Exception e){}try{ conn.close();//}catch(Exception e){}}return res;}
 
使用者在用完数据库连接后通常是直接调用连接的方法close来释放数据库资源，如果用我们前面提到的连接池的实现方法，那语句conn.close()将被某些特定的语句所替代。
第二：使连接池无法对之中的所有连接进行独占控制。由于连接池不允许用户直接调用连接的close方法，一旦使用者在使用的过程中由于习惯问题直接关闭了数据库连接，那么连接池将无法正常维护所有连接的状态，考虑连接池和应用由不同开发人员实现时这种问题更容易出现。
综合上面提到的两个问题，我们来讨论一下如何解决这两个要命的问题。
首先我们先设身处地的考虑一下用户是想怎么样来使用这个数据库连接池的。用户可以通过特定的方法来获取数据库的连接，同时这个连接的类型应该是标准的java.sql.Connection。用户在获取到这个数据库连接后可以对这个连接进行任意的操作，包括关闭连接等。
通过对用户使用的描述，怎样可以接管Connection.close方法就成了我们这篇文章的主题。
为了接管数据库连接的close方法，我们应该有一种类似于钩子的机制。例如在Windows编程中我们可以利用Hook API来实现对某个Windows API的接管。在JAVA中同样也有这样一个机制。JAVA提供了一个Proxy类和一个InvocationHandler，这两个类都在java.lang.reflect包中。我们先来看看SUN公司提供的文档是怎么描述这两个类的。
public interface InvocationHandler
InvocationHandler is the interface implemented by the invocation handler of a proxy instance. 
Each proxy instance has an associated invocation handler. When a method is invoked on a proxy instance, the method invocation is encoded and dispatched to the invoke method of its invocation handler.
 
SUN的API文档中关于Proxy的描述很多，这里就不罗列出来。通过文档对接口InvocationHandler的描述我们可以看到当调用一个Proxy实例的方法时会触发Invocationhanlder的invoke方法。从JAVA的文档中我们也同时了解到这种动态代理机制只能接管接口的方法，而对一般的类无效，考虑到java.sql.Connection本身也是一个接口由此就找到了解决如何接管close方法的出路。
首先，我们先定义一个数据库连接池参数的类，定义了数据库的JDBC驱动程序类名，连接的URL以及用户名口令等等一些信息，该类是用于初始化连接池的参数，具体定义如下：
public class ConnectionParam implements Serializable{ private String driver;    //数据库驱动程序 private String url;     //数据连接的URL private String user;     //数据库用户名 private String password;    //数据库密码 private int minConnection = 0;  //初始化连接数 private int maxConnection = 50;  //最大连接数 private long timeoutValue = 600000;//连接的最大空闲时间 private long waitTime = 30000;  //取连接的时候如果没有可用连接最大的等待时间
 
其次是连接池的工厂类ConnectionFactory，通过该类来将一个连接池对象与一个名称对应起来，使用者通过该名称就可以获取指定的连接池对象，具体代码如下：
/** * 连接池类厂，该类常用来保存多个数据源名称合数据库连接池对应的哈希 * @author liusoft */public class ConnectionFactory{ //该哈希表用来保存数据源名和连接池对象的关系表 static Hashtable connectionPools = null; static{  connectionPools = new Hashtable(2,0.75F); }  /**  * 从连接池工厂中获取指定名称对应的连接池对象  * @param dataSource 连接池对象对应的名称  * @return DataSource 返回名称对应的连接池对象  * @throws NameNotFoundException 无法找到指定的连接池  */ public static DataSource lookup(String dataSource)   throws NameNotFoundException {  Object ds = null;  ds = connectionPools.get(dataSource);  if(ds == null || !(ds instanceof DataSource))   throw new NameNotFoundException(dataSource);  return (DataSource)ds; }
 /**  * 将指定的名字和数据库连接配置绑定在一起并初始化数据库连接池  * @param name  对应连接池的名称  * @param param 连接池的配置参数，具体请见类ConnectionParam  * @return DataSource 如果绑定成功后返回连接池对象  * @throws NameAlreadyBoundException 一定名字name已经绑定则抛出该异常  * @throws ClassNotFoundException  无法找到连接池的配置中的驱动程序类  * @throws IllegalAccessException  连接池配置中的驱动程序类有误  * @throws InstantiationException  无法实例化驱动程序类  * @throws SQLException    无法正常连接指定的数据库  */ public static DataSource bind(String name, ConnectionParam param)  throws NameAlreadyBoundException,ClassNotFoundException,    IllegalAccessException,InstantiationException,SQLException {  DataSourceImpl source = null;  try{   lookup(name);   throw new NameAlreadyBoundException(name);  }catch(NameNotFoundException e){   source = new DataSourceImpl(param);   source.initConnection();   connectionPools.put(name, source);  }  return source; } /**  * 重新绑定数据库连接池  * @param name  对应连接池的名称  * @param param 连接池的配置参数，具体请见类ConnectionParam  * @return DataSource 如果绑定成功后返回连接池对象  * @throws NameAlreadyBoundException 一定名字name已经绑定则抛出该异常  * @throws ClassNotFoundException  无法找到连接池的配置中的驱动程序类  * @throws IllegalAccessException  连接池配置中的驱动程序类有误  * @throws InstantiationException  无法实例化驱动程序类  * @throws SQLException    无法正常连接指定的数据库  */ public static DataSource rebind(String name, ConnectionParam param)  throws NameAlreadyBoundException,ClassNotFoundException,    IllegalAccessException,InstantiationException,SQLException {  try{   unbind(name);  }catch(Exception e){}  return bind(name, param); } /**  * 删除一个数据库连接池对象  * @param name  * @throws NameNotFoundException  */ public static void unbind(String name) throws NameNotFoundException {  DataSource dataSource = lookup(name);  if(dataSource instanceof DataSourceImpl){   DataSourceImpl dsi = (DataSourceImpl)dataSource;   try{    dsi.stop();    dsi.close();   }catch(Exception e){   }finally{    dsi = null;   }  }  connectionPools.remove(name); } }
 
ConnectionFactory主要提供了用户将将连接池绑定到一个具体的名称上以及取消绑定的操作。使用者只需要关心这两个类即可使用数据库连接池的功能。下面我们给出一段如何使用连接池的代码：
 String name = "pool"; String driver = " sun.jdbc.odbc.JdbcOdbcDriver "; String url = "jdbc:odbc:datasource"; ConnectionParam param = new ConnectionParam(driver,url,null,null); param.setMinConnection(1); param.setMaxConnection(5); param.setTimeoutValue(20000); ConnectionFactory.bind(name, param); System.out.println("bind datasource ok."); //以上代码是用来登记一个连接池对象，该操作可以在程序初始化只做一次即可 //以下开始就是使用者真正需要写的代码 DataSource ds = ConnectionFactory.lookup(name); try{  for(int i=0;i&lt;10;i++){   Connection conn = ds.getConnection();   try{    testSQL(conn, sql);   }finally{    try{     conn.close();    }catch(Exception e){}   }  } }catch(Exception e){  e.printStackTrace(); }finally{  ConnectionFactory.unbind(name);  System.out.println("unbind datasource ok.");  System.exit(0); }
 
从使用者的示例代码就可以看出，我们已经解决了常规连接池产生的两个问题。但是我们最最关心的是如何解决接管close方法的办法。接管工作主要在ConnectionFactory中的两句代码：
source = new DataSourceImpl(param);source.initConnection();
 
DataSourceImpl是一个实现了接口javax.sql.DataSource的类，该类维护着一个连接池的对象。由于该类是一个受保护的类，因此它暴露给使用者的方法只有接口DataSource中定义的方法，其他的所有方法对使用者来说都是不可视的。我们先来关心用户可访问的一个方法getConnection
/** * @see javax.sql.DataSource#getConnection(String,String) */ public Connection getConnection(String user, String password) throws SQLException  {  //首先从连接池中找出空闲的对象  Connection conn = getFreeConnection(0);  if(conn == null){   //判断是否超过最大连接数,如果超过最大连接数   //则等待一定时间查看是否有空闲连接,否则抛出异常告诉用户无可用连接   if(getConnectionCount() &gt;= connParam.getMaxConnection())    conn = getFreeConnection(connParam.getWaitTime());   else{//没有超过连接数，重新获取一个数据库的连接    connParam.setUser(user);    connParam.setPassword(password);    Connection conn2 = DriverManager.getConnection(connParam.getUrl(),     user, password);    //代理将要返回的连接对象    _Connection _conn = new _Connection(conn2,true);    synchronized(conns){     conns.add(_conn);    }    conn = _conn.getConnection();   }  }  return conn; } /**  * 从连接池中取一个空闲的连接  * @param nTimeout 如果该参数值为0则没有连接时只是返回一个null  * 否则的话等待nTimeout毫秒看是否还有空闲连接，如果没有抛出异常  * @return Connection  * @throws SQLException  */ protected synchronized Connection getFreeConnection(long nTimeout)   throws SQLException {  Connection conn = null;  Iterator iter = conns.iterator();  while(iter.hasNext()){   _Connection _conn = (_Connection)iter.next();   if(!_conn.isInUse()){    conn = _conn.getConnection();    _conn.setInUse(true);        break;   }  }  if(conn == null &amp;&amp; nTimeout &gt; 0){   //等待nTimeout毫秒以便看是否有空闲连接   try{    Thread.sleep(nTimeout);   }catch(Exception e){}   conn = getFreeConnection(0);   if(conn == null)    throw new SQLException("没有可用的数据库连接");  }  return conn; }
 
DataSourceImpl类中实现getConnection方法的跟正常的数据库连接池的逻辑是一致的，首先判断是否有空闲的连接，如果没有的话判断连接数是否已经超过最大连接数等等的一些逻辑。但是有一点不同的是通过DriverManager得到的数据库连接并不是及时返回的，而是通过一个叫_Connection的类中介一下，然后调用_Connection.getConnection返回的。如果我们没有通过一个中介也就是JAVA中的Proxy来接管要返回的接口对象，那么我们就没有办法截住Connection.close方法。
终于到了核心所在，我们先来看看_Connection是如何实现的，然后再介绍是客户端调用Connection.close方法时走的是怎样一个流程，为什么并没有真正的关闭连接。
/** * 数据连接的自封装，屏蔽了close方法 * @author Liudong */class _Connection implements InvocationHandler{ private final static String CLOSE_METHOD_NAME = "close"; private Connection conn = null; //数据库的忙状态 private boolean inUse = false; //用户最后一次访问该连接方法的时间 private long lastAccessTime = System.currentTimeMillis();  _Connection(Connection conn, boolean inUse){  this.conn = conn;  this.inUse = inUse; } /**  * Returns the conn.  * @return Connection  */ public Connection getConnection() {  //返回数据库连接conn的接管类，以便截住close方法  Connection conn2 = (Connection)Proxy.newProxyInstance(   conn.getClass().getClassLoader(),   conn.getClass().getInterfaces(),this);  return conn2; } /**  * 该方法真正的关闭了数据库的连接  * @throws SQLException  */ void close() throws SQLException{  //由于类属性conn是没有被接管的连接，因此一旦调用close方法后就直接关闭连接  conn.close(); } /**  * Returns the inUse.  * @return boolean  */ public boolean isInUse() {  return inUse; }
 /**  * @see java.lang.reflect.InvocationHandler#invoke(java.lang.Object, java.lang.reflect.Method, java.lang.Object)  */ public Object invoke(Object proxy, Method m, Object[] args)   throws Throwable  {  Object obj = null;  //判断是否调用了close的方法，如果调用close方法则把连接置为无用状态  if(CLOSE_METHOD_NAME.equals(m.getName()))   setInUse(false);    else   obj = m.invoke(conn, args);   //设置最后一次访问时间，以便及时清除超时的连接  lastAccessTime = System.currentTimeMillis();  return obj; }   /**  * Returns the lastAccessTime.  * @return long  */ public long getLastAccessTime() {  return lastAccessTime; }
 /**  * Sets the inUse.  * @param inUse The inUse to set  */ public void setInUse(boolean inUse) {  this.inUse = inUse; }}
 
一旦使用者调用所得到连接的close方法，由于用户的连接对象是经过接管后的对象，因此JAVA虚拟机会首先调用_Connection.invoke方法，在该方法中首先判断是否为close方法，如果不是则将代码转给真正的没有被接管的连接对象conn。否则的话只是简单的将该连接的状态设置为可用。到此您可能就明白了整个接管的过程，但是同时也有一个疑问：这样的话是不是这些已建立的连接就始终没有办法真正关闭？答案是可以的。我们来看看ConnectionFactory.unbind方法，该方法首先找到名字对应的连接池对象，然后关闭该连接池中的所有连接并删除掉连接池。在DataSourceImpl类中定义了一个close方法用来关闭所有的连接，详细代码如下：
 /**  * 关闭该连接池中的所有数据库连接  * @return int 返回被关闭连接的个数  * @throws SQLException  */ public int close() throws SQLException {  int cc = 0;  SQLException excp = null;  Iterator iter = conns.iterator();  while(iter.hasNext()){   try{    ((_Connection)iter.next()).close();    cc ++;   }catch(Exception e){    if(e instanceof SQLException)     excp = (SQLException)e;   }  }  if(excp != null)   throw excp;  return cc; }
 
该方法一一调用连接池中每个对象的close方法，这个close方法对应的是_Connection中对close的实现，在_Connection定义中关闭数据库连接的时候是直接调用没有经过接管的对象的关闭方法，因此该close方法真正的释放了数据库资源。
以上文字只是描述了接口方法的接管，具体一个实用的连接池模块还需要对空闲连接的监控并及时释放连接，详细的代码请参照附件。
参考资料 
http://java.sun.com 
JAVA的官方网站
关于作者刘冬，珠海市创我科技发展有限公司软件工程师，主要从事J2EE方面的开发。电子邮件： winter.lau@163.com  
 



