---
layout:     post
title:      "使用OkHttp进行HTTPS连接"
date:       "2020-03-11 11:31:00"
author:     "Vincent"
image:  "img/home-bg-highway.jpg"
catalog: true
tags:
    - Java
    - OkHttp
    - SSL
---


## 背景

Java 搞个SSL居然还这么麻烦,翻了下官方文档.翻译下HTTPS 相关章节

OkHttp努力平滑下面的两个点

- **连接性** 尽可能的连接各种主机.这包含运行 [boringssl](https://boringssl.googlesource.com/boringssl/) 最新版本的高级主机以及运行[OpenSSL](https://www.openssl.org/)的旧主机.
- **连接的安全性**  这包括使用证书验证远程web服务器，以及使用强密码交换数据的隐私。

当协商连接到一个HTTPS 服务器时,OkHttp需要知道[TLS](http://square.github.io/okhttp/4.x/okhttp/okhttp3/-tls-version/)的版本和提供的[加密套件](http://square.github.io/okhttp/4.x/okhttp/okhttp3/-cipher-suite/).想要最大化的连接性的客户机,将包括过时的TLS版本和弱密码套件.一个想要最大限度地提高安全性的严格客户端将仅限于最新的TLS版本和最强的密码套件。

特定的安全性和连接性的决策由[ConnectionSpec](http://square.github.io/okhttp/4.x/okhttp/okhttp3/-connection-spec/)来提供。OkHttp包含四个内置连接规范：

- ```RESTRICTED_TLS``` 用于满足严格的合规需求的安全配置.
- ```MODERN_TLS``` 用于连接到现代的HTTPS服务器的安全配置.
- ```COMPATIBLE_TLS``` 用于连接安全但是不是当下的HTTPS服务器.
- ```CLEARTEXT``` 是一个不安全的配置,用于```http://```开头的URL.

这些松散地遵循Google云策略中设置的模型。我们跟踪此策略的更改.

OkHttp默认会使用```MODERN_TLS```进行连接.通过配置客户端的```ConnectionSpecs```你可以允许在```MODERN_TLS```失效的时候使用```COMPATIBLE_TLS```.代码如下

```java
OkHttpClient client = new OkHttpClient.Builder()
    .connectionSpecs(
        Arrays.asList(
            ConnectionSpec.MODERN_TLS, 
            ConnectionSpec.COMPATIBLE_TLS
            )
    )
    .build();
```

TLS版本和加密套件会在发布的时候进行更改.例如在OkHttp 2.2为了响应POODLE攻击,发布时我们放弃了支持 SSL 3.0 . 2.3版本时我们放弃了对RC4算法的支持.与桌面web浏览器一样，使用OkHttp保持最新是保持安全的最佳方式。

您可以使用一组自定义的TLS版本和密码套件来构建自己的连接规范。例如，此配置仅限于三个备受推崇的密码套件。它的缺点是需要Android 5.0+和类似的现代web服务器。

```java
ConnectionSpec spec = new ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
    .tlsVersions(TlsVersion.TLS_1_2)
    .cipherSuites(
          CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
          CipherSuite.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
          CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM_SHA256)
    .build();

OkHttpClient client = new OkHttpClient.Builder()
    .connectionSpecs(Collections.singletonList(spec))
    .build();
```

## 解决方案

翻译文档,翻译了一般,还是使用了暴力方法解决这个问题,就是信任所有的SSL证书.

定义了自己的```SSLSocketFactory```,```hostnameVerifier```,```trustManager``` 的实现

```java
package com.vnzmi.tool;

import javax.net.ssl.*;
import java.security.SecureRandom;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

public class TrustAll {
    public static SSLSocketFactory socketFactory() {
        SSLSocketFactory ssfFactory = null;

        try {
            SSLContext sc = SSLContext.getInstance("TLS");
            sc.init(null, new TrustManager[]{new trustManager()}, new SecureRandom());

            ssfFactory = sc.getSocketFactory();
        } catch (Exception e) {
        }

        return ssfFactory;
    }

    public static class hostnameVerifier implements HostnameVerifier {
        @Override
        public boolean verify(String hostname, SSLSession session) {
            return true;
        }
    }

    public static class trustManager implements X509TrustManager, TrustManager {
        @Override
        public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {
        }

        @Override
        public void checkClientTrusted(X509Certificate[] x509Certificates, String s) throws CertificateException {

        }

        @Override
        public X509Certificate[] getAcceptedIssuers() {
            return new X509Certificate[0];
        }
    }
}
```

使用方法如下:

```java
public TemplateInfo[] readMetaData() {
        OkHttpClient client = null;
        try {
            client = new OkHttpClient.Builder()
                    .connectionSpecs(Arrays.asList(ConnectionSpec.MODERN_TLS, ConnectionSpec.COMPATIBLE_TLS))
                    .sslSocketFactory(TrustAll.socketFactory(), new TrustAll.trustManager())
                    .hostnameVerifier(new TrustAll.hostnameVerifier())
                    .build();
        } catch (Exception e) {
            e.printStackTrace();
        }
        Request request = new Request.Builder().url(url).build();

        TemplateInfo[]  templateInfos= new TemplateInfo[0];

        //CodeSketch.info(request.toString());

        try (Response response = client.newCall(request).execute()) {
            InputStream is = response.body().byteStream();
            ObjectMapper om = new ObjectMapper();
            templateInfos = om.readValue(is, TemplateInfo[].class);
            /*CodeSketch.info(templateInfos.length);
            for (int i = 0; i < templateInfos.length; i++) {
                System.out.println(templateInfos[i]);
            }*/
        } catch (IOException e) {
            e.printStackTrace();
        }
        return templateInfos;
    }
```

这段代码是 code sketch读取服务端的模板列表.进行模板下载的.这部分功能还没开发完成.

[https://github.com/vincentmi/codesketch](https://github.com/vincentmi/codesketch)
 








 

