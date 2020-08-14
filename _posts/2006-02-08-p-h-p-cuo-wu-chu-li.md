---
layout:     post
title:      "php错误处理"
date:       2006-02-08 15:22:38
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: true
tags:
    - 新浪博客
    - 技术文章
---




 
PHP 有如下几种错误和警告： 

表格 16-1. PHP 错误类型



值
常量
描述
备注


1
E_ERROR
运行时致命错误
 

2
E_WARNING
运行时警告（非致命错误）
 

4
E_PARSE
编译时解析错误
 

8
E_NOTICE 
运行时提醒（比 Warning 的严重性更低） 
 

16
E_CORE_ERROR
在 PHP 初始化过程中发生的致命错误
仅 PHP 4 有效

32
E_CORE_WARNING
在 PHP 初始化过程中发生的警告（非指明错误） 
仅 PHP 4 有效

64
E_COMPILE_ERROR
编译时指明错误
仅 PHP 4 有效

128
E_COMPILE_WARNING
编译时警告（非指明错误）
仅 PHP 4 有效

256
E_USER_ERROR
用户自定义错误信息
仅 PHP 4 有效

512
E_USER_WARNING
用户自定义警告信息
仅 PHP 4 有效

1024
E_USER_NOTICE 
用户自定义提醒信息
仅 PHP 4 有效

 
E_ALL
以上所有支持的项目
 

以上的值（不管是数字还是符号）被用来建立指定要报告的错误的位掩码（bitmask）。您可以使用位操作符来叠加或者掩去某一种类型的错误。请注意 php.ini 仅能识别“|”、“~”、“!”和“&amp;”四种符号，而 php3.ini 无法识别任何位操作符。 
在 PHP 4 中，error_reporting 默认的值为 E_ALL &amp; ~E_NOTICE，表示显示除 E_NOTICE-level 以外所有错误的警告信息。在 PHP 3 中，其默认值为 (E_ERROR | E_WARNING | E_PARSE)，表示的内容和 PHP 4 相同。注意，由于 php3.ini 不支持常量，error_reporting 的设置应该用数字来表示，因此，其值应该为 7。 
这项设置的初始设定可以通过更改 ini 文件中的 error_reporting 选项来改变，也可以在 Apache 系统中设置 httpd.conf 中的 php_error_reporting（PHP 3 为 php3_error_reporting）来改变。另外，脚本的运行过程中，也可以通过 error_reporting() 函数来更改该设置。 





警告


在将服务端的代码从 PHP 3 升级到 PHP 4 时，您需要检查这些设置，或者调用 error_reporting()，否则您可能会屏蔽新类型的错误报告，尤其是 E_COMPILE_ERROR。这将有可能导致没有任何反馈信息的空文档，使得您不知道发生了什么，也不知道到哪里检查发生的问题。 
所有的 PHP 表达式都可以使用“@”前缀，该前缀将屏蔽该表达式所有的错误信息。如果在该语句运行过程中出现了错误并且 track_errors 选项开启，则您可以在全局变量 $php_errormsg 中找到错误信息。 


注: @ 错误信息控制符前缀不会屏蔽解析错误信息。 





警告


目前 @ 错误信息控制符前缀有可能会屏蔽导致脚本停止运行的关键错误的信息。这也就是说，如果您在不可用的，或者未正确定义的函数前面使用 @ 符号来抑制错误，脚本程序会在该处停止运行，并且不会给出任何关于为什么停止的提示信息。 
以下是在 PHP 中使用错误处理兼容的例子。我们定义了一个错误处理函数，该函数会将错误信息记录到一个文件中（用 XML 格式），并在脚本出现关键错误时将错误信息通过 Email 发送给开发者。 





例子 16-1. 在脚本中使用错误处理



&lt;?php
// we will do our own error handling
error_reporting(0);

// user defined error handling function
function userErrorHandler ($errno, $errmsg, $filename, $linenum, $vars) {
    // timestamp for the error entry
    $dt = date("Y-m-d H:i:s (T)");

    // define an assoc array of error string
    // in reality the only entries we should
    // consider are 2,8,256,512 and 1024
    $errortype = array (
                1   =&gt;  "Error",
                2   =&gt;  "Warning",
                4   =&gt;  "Parsing Error",
                8   =&gt;  "Notice",
                16  =&gt;  "Core Error",
                32  =&gt;  "Core Warning",
                64  =&gt;  "Compile Error",
                128 =&gt;  "Compile Warning",
                256 =&gt;  "User Error",
                512 =&gt;  "User Warning",
                1024=&gt;  "User Notice"
                );
    // set of errors for which a var trace will be saved
    $user_errors = array(E_USER_ERROR, E_USER_WARNING, E_USER_NOTICE);
    
    $err = "&lt;errorentry&gt;\n";
    $err .= "\t&lt;datetime&gt;".$dt."&lt;/datetime&gt;\n";
    $err .= "\t&lt;errornum&gt;".$errno."&lt;/errornum&gt;\n";
    $err .= "\t&lt;errortype&gt;".$errortype[$errno]."&lt;/errortype&gt;\n";
    $err .= "\t&lt;errormsg&gt;".$errmsg."&lt;/errormsg&gt;\n";
    $err .= "\t&lt;scriptname&gt;".$filename."&lt;/scriptname&gt;\n";
    $err .= "\t&lt;scriptlinenum&gt;".$linenum."&lt;/scriptlinenum&gt;\n";

    if (in_array($errno, $user_errors))
        $err .= "\t&lt;vartrace&gt;".wddx_serialize_value($vars,"Variables")."&lt;/vartrace&gt;\n";
    $err .= "&lt;/errorentry&gt;\n\n";
    
    // for testing
    // echo $err;

    // save to the error log, and e-mail me if there is a critical user error
    error_log($err, 3, "/usr/local/php4/error.log");
    if ($errno == E_USER_ERROR)
        mail("phpdev@example.com","Critical User Error",$err);
}


function distance ($vect1, $vect2) {
    if (!is_array($vect1) || !is_array($vect2)) {
        trigger_error("Incorrect parameters, arrays expected", E_USER_ERROR);
        return NULL;
    }

    if (count($vect1) != count($vect2)) {
        trigger_error("Vectors need to be of the same size", E_USER_ERROR);
        return NULL;
    }

    for ($i=0; $i&lt;count($vect1); $i++) {
        $c1 = $vect1[$i]; $c2 = $vect2[$i];
        $d = 0.0;
        if (!is_numeric($c1)) {
            trigger_error("Coordinate $i in vector 1 is not a number, using zero", 
                            E_USER_WARNING);
            $c1 = 0.0;
        }
        if (!is_numeric($c2)) {
            trigger_error("Coordinate $i in vector 2 is not a number, using zero", 
                            E_USER_WARNING);
            $c2 = 0.0;
        }
        $d += $c2*$c2 - $c1*$c1;
    }
    return sqrt($d);
}

$old_error_handler = set_error_handler("userErrorHandler");

// undefined constant, generates a warning
$t = I_AM_NOT_DEFINED;

// define some "vectors"
$a = array(2,3,"foo");
$b = array(5.5, 4.3, -1.6);
$c = array (1,-3);

// generate a user error
$t1 = distance($c,$b)."\n";

// generate another user error
$t2 = distance($b,"i am not an array")."\n";

// generate a warning
$t3 = distance($a,$b)."\n";

?&gt;这仅仅是关于错误处理和记录函数的一个简单的例子。 
请参阅 error_reporting(), error_log(), set_error_handler(), restore_error_handler(), trigger_error(), user_error() 
 





转移自: (http://blog.sina.com.cn/s/blog_542a3955010001w5.html)[http://blog.sina.com.cn/s/blog_542a3955010001w5.html]