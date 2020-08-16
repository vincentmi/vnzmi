---
layout:     post
title:      "Java动态程序设计：反射介绍"
date:       2006-04-21 15:30:16
author:     "Vincent"
header-img:  "img/post-bg-dot.jpg"
catalog: false
tags:
    - 新浪博客
    - 技术文章
---


Java动态程序设计：反射介绍使用运行的类的信息使你的程序设计更加灵活反射授予了你的代码访问装载进JVM内的Java类的内部信息的权限，并且允许你编写在程序执行期间与所选择的类的一同工作的代码，而不是在源代码中。这种机制使得反射成为创建灵活的应用程序的强大工具，但是要小心的是，如果使用不恰当，反射会带来很大的副作用。在这篇文章中，软件咨询顾问Dennis Sosnoski 介绍了反射的使用，同时还介绍了一些使用反射所要付出的代价。在这里，你可以找到Java反射API是如何在运行时让你钩入对象的。在第一部分，我向你介绍了Java程序设计的类以及类的装载。那篇文章中描述了很多出现在Java二进制类格式中的信息，现在我来介绍在运行时使用反射API访问和使用这些信息的基础。为了使那些已经了解反射基础的开发人员对这些事情感兴趣，我还会介绍一些反射与直接访问的在性能方面的比较。使用反射与和metadata(描述其它数据的数据)一些工作的Java程序设计是不同的。通过Java语言反射来访问的元数据的特殊类型是在JVM内部的类和对象的描述。反射使你可以在运行时访问各种类信息，它甚至可以你让在运行时读写属性字段、调用所选择的类的方法。反射是一个强大的工具，它让你建立灵活能够在运行时组装的代码，而不需要连接组件间的源代码。反射的一些特征也带来一些问题。在这章中，我将会探究在应用程序中不打算使用反射的原因，以为什么使用它的原因。在你了解到这些利弊之后，你就会在好处大于缺点的时候做出决定。初识class使用反射的起点总时一个java.lang.Class类的实例。如果你与一个预先确定的类一同工作，Java语言为直接获得Class类的实例提供了一个简单的快捷方式。例如：Class clas = MyClass.class;当你使用这项技术的时候，所有与装载类有关的工作都发生在幕后。如果你需要在运行时从外部的资源中读取类名，使用上面这种方法是不会达到目的的，相反你需要使用类装载器来查找类的信息，方法如下所示：

```java
// "name" is the class name to loadClass 
clas = null;
try {  
    clas = Class.forName(name);
} catch (ClassNotFoundException ex) {
      // handle exception case
}// use the loaded class

```

如果类已经装载，你将会找到当前在在的类的信息。如果类还没有被装载，那么类装载器将会装载它，并且返回最近创建的类的实例。关于类的反射Class对象给予你了所有的用于反射访问类的元数据的基本钩子。这些元数据包括有关类的自身信息，例如象类的包和子类，还有这个类所实现的接口，还包括这个类所定义的构造器、属性字段以及方法的详细信息。后面的这些项是我们在程序设计过种经常使用的，因此在这一节的后面我会给出一些用这些信息来工作的例子。对于类的构造中的每一种类型（构造器、属性字段、方法），java.lang.Class提供了四种独立的反射调用以不的方式来访问类的信息。下面列出了这四种调用的标准形式，它是一组用于查找构造器的调用。Constructor getConstructor(Class[] params)   使用指定的参数类型来获得公共的构造器；Constructor[] getConstructors()    获得这个类的所有构造器；Constructor getDeclaredConstructor(Class[] params) 使用指定的参数类型来获得构造器（忽略访问的级别）Constructor[] getDeclaredConstructors()  获得这个类的所有的构造器（忽略访问的级别）上述的每一种方法都返回一或多个java.lang.reflect.Constructor的实例。Constructor类定义了一个需要一个对象数据做为唯一参数的newInstance方法，然后返回一个最近创建的原始类的实例。对象数组是在构造器调用时所使用的参数值。例如，假设你有一个带有一对String 类型做为参数的构造器的TwoString类，代码如下所示：public class TwoString {    private String m_s1, m_s2;    public TwoString(String s1, String s2) {        m_s1 = s1;        m_s2 = s2;    }}下面的代码显示如何获得TwoString类的构造器，并使用字符串“a”和“b”来创建一个实例：Class[] types = new Class[] { String.class, String.class };    Constructor cons = TwoString.class.getConstructor(types);    Object[] args = new Object[] { "a", "b" };    TwoString ts = cons.newInstance(args);上面的代码忽略了几种可能的被不同的反射方法抛出的异常检查的类型。这些异常在Javadoc　API中有详细的描述，因此为简便起见，我会在所有的代码中忽略它们。在我涉及到构造器这个主题时，Java语言也定义了一个特殊的没有参数的（或默认）构造器快捷方法，你能使用它来创建一个类的实例。这个快捷方法象下面的代码这样被嵌入到类的自定义中：Object newInstance() ?使用默认的构造器创建新的实例。尽管这种方法只让你使用一个特殊的构造器，但是如果你需要的话，它是非常便利的快捷方式。这项技术在使用JavaBeans工作的时候尤其有用，因为JavaBeans需要定义一个公共的、没有参数的构造器。通过反射来查找属性字段Class类反射调用访问属性字段信息与那些用于访问构造器的方法类似，在有数组类型的参数的使用属性字段名来替代：使用方法如下所示：Field getField(String name)  --获得由name指定的具有public级别的属性字段Field getFields() ?获得一个类的所有具有public级别的属性字段Field getDeclaredField(String name) ?获得由name指定的被类声明的属性字段Field getDeclaredFields() ?获得由类定义的所有的属性字段尽管与构造器的调用很相似，但是在提到属性字段的时候，有一个重要的差别：前两个方法返回能过类来访问的公共（public）属性字段的信息（包括那些来自于超类的属性字段），后两个方法返回由类直接声明的所有的属性字段（忽略了属性字段的访问类型）。Java.lang.reflect.Field的实例通过调用定义好的getXXX和setXXX方法来返回所有的原始的数据类型，就像普通的与对象引用一起工作的get和set方法一样。尽管getXXX方法会自动地处理数据类型转换（例如使用getInt方法来获取一个byte类型的值），但使用一个适当基于实际的属性字段类型的方法是应该优先考虑的。下面的代码显示了如何使用属性字段的反射方法，通过指定属性字段名，找到一个对象的int类型的属性字段，并给这个属性字段值加1。public int incrementField(String name, Object obj) throws... {    Field field = obj.getClass().getDeclaredField(name);    int value = field.getInt(obj) + 1;    field.setInt(obj, value);    return value;}这个方法开始展现一些使用反射所可能带来的灵活性，它优于与一个特定的类一同工作，incrementField方法把要查找的类信息的对象传递给getClass方法，然后直接在那个类中查找命名的属性字段。通过反射来查找方法Class反射调用访问方法的信息与访问构造器和字段属性的方法非常相似：    Method getMethod(String name,Class[] params)  --使用指定的参数类型获得由name参数指定的public类型的方法。Mehtod[] getMethods()?获得一个类的所有的public类型的方法Mehtod getDeclaredMethod(String name, Class[] params)?使用指定的参数类型获得由name参数所指定的由这个类声明的方法。Method[] getDeclaredMethods() ?获得这个类所声明的所有的方法与属性字段的调用一样，前两个方法返回通过这个类的实例可以访问的public类型的方法?包括那些继承于超类的方法。后两个方法返回由这个类直接声明的方法的信息，而不管方法的访问类型。通过调用返回的Java.lang.reflect.Mehtod实例定义了一个invoke方法，你可以使用它来调用定义类的有关实例。这个invoke方法需要两个参数，一个是提供这个方法的类的实例，一个是调用这个方法所需要的参数值的数组。下面给出了比属性字段的例子更加深入的例子，它显示了一个的方法反射的例子，这个方法使用get和set方法来给JavaBean定义的int类型的属性做增量操作。例如，如果对象为一个整数类型count属性定义了getCount和setCount方法，那么为了给这个属性做增量运算，你就可以把“count”做为参数名传递给调用的这个方法中。示例代码如下：public int incrementProperty(String name, Object obj) {    String prop = Character.toUpperCase(name.charAt(0)) +        name.substring(1);    String mname = "get" + prop;    Class[] types = new Class[] {};    Method method = obj.getClass().getMethod(mname, types);    Object result = method.invoke(obj, new Object[0]);    int value = ((Integer)result).intValue() + 1;    mname = "set" + prop;    types = new Class[] { int.class };    method = obj.getClass().getMethod(mname, types);    method.invoke(obj, new Object[] { new Integer(value) });    return value;}根据JavaBeans的规范，我把属性名的第一个字母转换为大写，然后在前面加上“get”来建立读取属性值的方法名，在属性名前加上“set”来建立设置属性值的方法名。JavaBeans的读方法只返回属性值，写方法只需要要写入的值做为参数，因此我指定了与这个方法相匹配的参数类型。最后规范规定这两个方法应该是public类型的，因此我使用了查找相关类的public类型方法的调用形式。这个例子我首先使用反射传递一个原始类型的值，因此让我们来看一下它是怎样工作的。基本的原理是简单的：无论什么时候，你需要传递一个原始类型的值，你只要替换相应的封装原始类型的（在java.lang 包中定义的）的类的实例就可以了。这种方法可应用于调用和返回。因此在我的例子中调用get方法时，我预期的结果是一个由java.lang.Integer类所封装的实际的int类型的属性值。



