---
layout:     post
title:      "CXF添加Header"
date:       2015-05-10 23:16:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - WS
    - CXF
---

CXF的header处理了半天。。。

添加拦截器


```java
    
public class HotelHeaderInterceptor extends AbstractSoapInterceptor {
public void handleMessage(SoapMessage message) throws Fault {
		    
		    List<Header> headers = message.getHeaders(); 
		 
		    AuthenticationHeader aheader = new AuthenticationHeader();
		    aheader.setCulture(com.tourico.schemas.webservices.authentication.Culture.EN_US);
		    aheader.setLoginName(username);
		    aheader.setPassword(password);
		    aheader.setVersion(new JAXBElement<String>(new QName("", "version"), String.class, version));
		    
		    JAXBElement<AuthenticationHeader> authHeaders = new ObjectFactory().createAuthenticationHeader(aheader);
		    
		    Header header;
			try {
				header = new Header(authHeaders.getName(), aheader,new JAXBDataBinding(AuthenticationHeader.class));
				headers.add(header);
			    message.put(Header.HEADER_LIST, headers);
			} catch (JAXBException e) {
				
				e.printStackTrace();
			}
	}
```


调用服务之前处理

```java
    IDestinationContracts  port = service.getIISDestinationHosting() ;
			Client cxfClient = ClientProxy.getClient(port);
			
			cxfClient.getOutInterceptors().add(new HeaderInterceptor(Phase.WRITE));
```


