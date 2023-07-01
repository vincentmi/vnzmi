---
layout:     post
title:      "扩展Thymeleaf-2  方言和处理器"
date:       2015-07-23 09:27:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - Spring
    - Thymeleaf
---
gitbook [http://vincentmi.gitbooks.io/extendingthymeleaf/content/][1]

如果你读过Thymeleaf的入门教程（你应该已经读完了）。你应该知道你之前学的准确的说不是Thymeleaf，而是Thymeleaf的标准方言。（或者，如果你读过Thymeleaf+Spring教程的话就是Spring标准方言）。

这是什么意思？意思是你学的th:xattribute只是可以立即使用的标准方言。但是你可以使用你喜欢的名字自己定义一组attribute或者tag在Thymeleaf用来处理你的模板。你可以定义你自己的方言。


<!--more-->


Dialects 是实现了org.thymeleaf.dialect.IDialect 接口的对象, 接口是这样的:

```
public interface IDialect {

    public String getPrefix();

    public Set<IProcessor> getProcessors();
    public Map<String,Object> getExecutionAttributes();

    public Set<IDocTypeTranslation> getDocTypeTranslations();
    public Set<IDocTypeResolutionEntry> getDocTypeResolutionEntries();
}```

让我们一步步来看他的方法:

首先, 前缀:

    public String getPrefix();

这是你方言的tag和attribute的前缀，一种命名空间(它在添加到模板引擎时可以被改变）。如果你添加了一个attribute 为 ```earth``` 而你的方言的前缀是```planets```,你在模板里将你的attribute可以写成```planets:earth```.

标准方言和Spring标准方言是 th.前缀可以是null.所以你可以为没有前缀的attribute和tag定义处理器。（例如：标准的XHTML标签<p> ,<div> <table>）

现在，让我们看看IDialect接口最重要的部分，处理器：

    public Set<IProcessor> getProcessors();
 
处理器是主要在DOM节点上执行和进行变化的对象。我们将会在下一章节介绍更多细节。

执行属性是在模板处理过程中为方言提供执行参数的一些对象。这些对象（usually utility objects通常是通用对象）将在执行器执行时可以使用。注意这些对象不会存在变量上下文中，只能在内部可见。

    public Map<String,Object> getExecutionAttributes();

更多接口方法:

    public Set<IDocTypeTranslation> getDocTypeTranslations();

这个将返回一个DCOTYPE转换的集合.如果你记得入门教程。Thymeleaf可以处理一系列DOCTYPE的转换.这样允许你为你的模板指定一个转换，将你的DOCTYPE在输出时转换为另一个DOCTYPE .

最后一个方法:

    public Set<IDocTypeResolutionEntry> getDocTypeResolutionEntries();

This method returns the DOCTYPE resolution entries available for the dialect. DOCTYPE resolution entries allow Thymeleaf’s XML Parser to locally resolve DTDs linked from your templates (从而避免远程检索这些DTD).

通过让你的方言实现抽象类 ```org.thymeleaf.dialect.AbstractXHTMLEnabledDialect```，Thymeleaf让大部分标准的XHTML DTD可用。但是你可以继续为你自己模板添加DTD。


## 处理器

处理器需要实现```org.thymeleaf.processor.IProcessor``` 接口, 它们包含了应用到DOM节点的真实逻辑. 接口定于如下:

     public interface IProcessor extends Comparable<IProcessor> {

     public IProcessorMatcher<? extends Node> getMatcher();

     public ProcessorResult process(final Arguments arguments,final ProcessorMatchingContext processorMatchingContext, final Node node);
     }


首先我们可以看到，它扩展自Comparable接口，这是它确定优先级的方式。如果一个处理器排在另外一前面。他就有更高的优先级，这样他讲会比后面的更早的再相同的节点执行。

现在看方法。一个matcher建立来匹配一个处理器是否可以应用到一个DOM节点:

    public IProcessorMatcher<? extends Node> getMatcher();
    
Matcher对象将检查节点的类型、名字和或属性（如果是一个DOM节点元素），如果是其他节点元素其他的节点特性也会被用来检查处理器是否可用。Thymeleaf附带一组预定义的IProcessorMatcher实现,这样您不必执行常见的任务，像通过它的名称或者它的一个属性匹配元素标记。   

最终这个方法做真正的工作：

    public ProcessorResult process(final Arguments arguments,
                final ProcessorMatchingContext processorMatchingContext, final Node node);
                
                
                
process(...) 有三个参数:

org.thymeleaf.Arguments对象的执行参数包含上下文、局部变量、模板解析信息和其他一些DOM处理的有用的数据。

处理器匹配上下文，其中包含有关执行处理器正在执行的条件的信息，实际上是匹配的。

问题在于相同的处理器类可以被包含在多个方言，在一个相同的模板引起中执行。可能配置会有所不同。单这些方言可能使用不同的前缀。如果这，我们怎么知道处理器执行的是哪个方言？这就是ProcessorMatchingContext对象的功能。

node是处理器将会执行的节点。注意这个处理器是应用到了特定的节点。但是并没有阻止这个节点树的其他部分的修改。

Thymeleaf提供一个抽象工具类，用于扩展处理器，```org.thymeleaf.processor.AbstractProcessor``` 这个类实现Comparable接口。定义了获得本地化和国际化的标准机制:

     public abstract class AbstractProcessor implements IProcessor {

    /* Try to resolve a message first as template message, then if not */
    /* found as processor message.                                     */
    protected String getMessage(
                final Arguments arguments, final String messageKey, 
                final Object[] messageParameters) {...}

    /* Try to resolve a message as a template message */
    protected String getMessageForTemplate(
                final Arguments arguments, final String messageKey, 
                final Object[] messageParameters) {...}

    /* Try to resolve a message as a processor message */
    protected String getMessageForProcessor(
                final Arguments arguments, final String messageKey, 
                final Object[] messageParameters) {...}

    public abstract int getPrecedence();

    ...

      }
      
      
### 特殊类型的处理器

虽然处理器可以在任何DOM树上执行。Thymeleaf内部执行引擎有两种特别类型的处理器用于提高效率：属性处理器和元素处理器。


### 属性处理器 (Attribute Processor)

这些处理器（实现了IProcessor接口）的getMatcher()方法返回一个```org.thymeleaf.processor.IAttributeNameProcessorMatcher```的实现，我们称为"属性处理器"。

因为这类Matcher定义了这些处理器将在DOM元素（通常是XML\HTML\HTML标签）包含了一个指定名称的属性时被触发。例如：在标准方言中，为th:text,th:each,th:if等等属性定义了Matcher。

为了简单起见，Thymeleaf提供了一个抽象类 ```org.thymeleaf.processor.attr.AbstractAttrProcessor``` 可以用来扩展为你自己的属性处理器。这个类已经实现了getMatcher方法，返回一个实现IAttributeNameProcessorMatcher接口的Matcher,让你更容易创建这类处理器。

### 元素处理器 (Element Processors)

这类处理器的getMatcher()方法返回一个```org.thymeleaf.processor.IElementNameProcessorMatcher```接口的实现被称为元素处理器。

注意,DOM行话所说的“元素”,在XML HTML5 /XHTML文档我们通常称之为“标签”。Thymeleaf喜欢使用更通用的“元素”这个词,因为**模板模式**可能被定义为工作在一个非XML类似结构的文档中。

这类matcher定义这些处理器在找到一个指定名称的元素时触发。

标准方言没有定于元素处理器。

简单起见，Thymeleaf也提供一个抽象类```org.thymeleaf.processor.element.AbstractElementProcessor```用来扩展成元素处理器。这个类已经实现了getMatcher返回一个IElementNameProcessorMatcher的实现，以便更容易的创建这类处理器。