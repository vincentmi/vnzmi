---
layout:     post
title:      "在b/s开发中经常用到的javaScript技术"
date:       2006-04-26 00:31:52
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: false
tags:
    - 新浪博客
    - 技术文章
---

在b/s开发中经常用到的javascript技术 一、验证类 1、数字验证内 1.1 整数 1.2 大于0的整数 （用于传来的ID的验证) 1.3 负整数的验证 1.4 整数不能大于iMax 1.5 整数不能小于iMin 2、时间类 2.1 短时间，形如 (13:04:06) 2.2 短日期，形如 (2003-12-05) 2.3 长时间，形如 (2003-12-05 13:04:06) 2.4 只有年和月。形如(2003-05,或者2003-5) 2.5 只有小时和分钟,形如(12:03) 3、表单类 3.1 所有的表单的值都不能为空 3.2 多行文本框的值不能为空。 3.3 多行文本框的值不能超过sMaxStrleng 3.4 多行文本框的值不能少于sMixStrleng 3.5 判断单选框是否选择。 3.6 判断复选框是否选择. 3.7 复选框的全选，多选，全不选，反选 3.8 文件上传过程中判断文件类型 4、字符类 4.1 判断字符全部由a-Z或者是A-Z的字字母组成 4.2 判断字符由字母和数字组成。 4.3 判断字符由字母和数字，下划线,点号组成.且开头的只能是下划线和字母 4.4 字符串替换函数.Replace(); 5、浏览器类 5.1 判断浏览器的类型 5.2 判断ie的版本 5.3 判断客户端的分辨率 6、结合类 6.1 email的判断。 6.2 手机号码的验证 6.3 身份证的验证 二、功能类 1、时间与相关控件类 1.1 日历 1.2 时间控件 1.3 万年历 1.4 显示动态显示时钟效果（文本，如OA中时间） 1.5 显示动态显示时钟效果 (图像，像手表) 2、表单类 2.1 自动生成表单 2.2 动态添加，修改，删除下拉框中的元素 2.3 可以输入内容的下拉框 2.4 多行文本框中只能输入iMax文字。如果多输入了，自动减少到iMax个文字（多用于短信发送) 3、打印类 3.1 打印控件 4、事件类 4.1 屏蔽右键 4.2 屏蔽所有功能键 4.3 --> 和<-- F5 F11,F9,F1 4.4 屏蔽组合键ctrl+N 5、网页设计类 5.1 连续滚动的文字，图片（注意是连续的，两段文字和图片中没有空白出现） 5.2 html编辑控件类 5.3 颜色选取框控件 5.4 下拉菜单 5.5 两层或多层次的下拉菜单 5.6 仿IE菜单的按钮。（效果如rongshuxa.com的导航栏目) 5.7 状态栏，title栏的动态效果（例子很多，可以研究一下） 5.8 双击后，网页自动滚屏 6、树型结构。 6.1 asp+SQL版 6.2 asp+xml+sql版 6.3 java+sql或者java+sql+xml 7、无边框效果的制作 8、连动下拉框技术 9、文本排序 一、验证类 1、数字验证内 1.1 整数 /^(-|+)?d+$/.test(str) 1.2 大于0的整数 （用于传来的ID的验证) /^d+$/.test(str) 1.3 负整数的验证 /^-d+$/.test(str) 2、时间类 2.1 短时间，形如 (13:04:06) function isTime(str) { var a = str.match(/^(d{1,2})(:)?(d{1,2})2(d{1,2})$/); if (a == null) {alert('输入的参数不是时间格式'); return false;} if (a[1]>24 || a[3]>60 || a[4]>60) { alert("时间格式不对"); return false } return true; } 2.2 短日期，形如 (2003-12-05) function strDateTime(str) { var r = str.match(/^(d{1,4})(-|/)(d{1,2})2(d{1,2})$/); if(r==null)return false; var d= new Date(r[1], r[3]-1, r[4]); return (d.getFullYear()==r[1]&&(d.getMonth()+1)==r[3]&&d.getDate()==r[4]); } 2.3 长时间，形如 (2003-12-05 13:04:06) function strDateTime(str) { var reg = /^(d{1,4})(-|/)(d{1,2})2(d{1,2}) (d{1,2}):(d{1,2}):(d{1,2})$/; var r = str.match(reg); if(r==null)return false; var d= new Date(r[1], r[3]-1,r[4],r[5],r[6],r[7]); return (d.getFullYear()==r[1]&&(d.getMonth()+1)==r[3]&&d.getDate()==r[4]&&d.getHours()==r[5]&&d.getMinutes()==r[6]&&d.getSeconds()==r[7]); } 2.4 只有年和月。形如(2003-05,或者2003-5) 2.5 只有小时和分钟,形如(12:03) 3、表单类 3.1 所有的表单的值都不能为空

3.2 多行文本框的值不能为空。 3.3 多行文本框的值不能超过sMaxStrleng 3.4 多行文本框的值不能少于sMixStrleng 3.5 判断单选框是否选择。 3.6 判断复选框是否选择. 3.7 复选框的全选，多选，全不选，反选 3.8 文件上传过程中判断文件类型 4、字符类 4.1 判断字符全部由a-Z或者是A-Z的字字母组成

4.2 判断字符由字母和数字组成。

4.3 判断字符由字母和数字，下划线,点号组成.且开头的只能是下划线和字母 /^([a-zA-z_]{1})([w]*)$/g.test(str) 4.4 字符串替换函数.Replace(); 5、浏览器类 5.1 判断浏览器的类型 window.navigator.appName 5.2 判断ie的版本 window.navigator.appVersion 5.3 判断客户端的分辨率 window.screen.height; window.screen.width; 6、结合类 6.1 email的判断。 function ismail(mail) { return(new RegExp(/^w+((-w+)|(.w+))*@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+)*.[A-Za-z0-9]+$/).test(mail)); } 6.2 手机号码的验证 6.3 身份证的验证 function isIdCardNo(num) { if (isNaN(num)) {alert("输入的不是数字！"); return false;} var len = num.length, re; if (len == 15) re = new RegExp(/^(d{6})()?(d{2})(d{2})(d{2})(d{3})$/); else if (len == 18) re = new RegExp(/^(d{6})()?(d{4})(d{2})(d{2})(d{3})(d)$/); else {alert("输入的数字位数不对！"); return false;} var a = num.match(re); if (a != null) { if (len==15) { var D = new Date("19"+a[3]+"/"+a[4]+"/"+a[5]); var B = D.getYear()==a[3]&&(D.getMonth()+1)==a[4]&&D.getDate()==a[5]; } else { var D = new Date(a[3]+"/"+a[4]+"/"+a[5]); var B = D.getFullYear()==a[3]&&(D.getMonth()+1)==a[4]&&D.getDate()==a[5]; } if (!B) {alert("输入的身份证号 "+ a[0] +" 里出生日期不对！"); return false;} } return true; } 3.7 复选框的全选，多选，全不选，反选
全选全选
language=javascript>
function checkAll(str)
{
  var a = document.getElementsByName(str);
  var n = a.length;
  for (var i=0; i

3.8 文件上传过程中判断文件类型  画图:
 

S.DrawingSurface.ArcDegrees(0,0,0,30,50,60);
S.DrawingSurface.ArcRadians(30,0,0,30,50,60);
S.DrawingSurface.Line(10,10,100,100);

写注册表：

var WshShell = WScript.CreateObject("WScript.Shell");
WshShell.RegWrite ("HKCUSoftwareACMEFortuneTeller", 1, "REG_BINARY");
WshShell.RegWrite ("HKCUSoftwareACMEFortuneTellerMindReader", "Goocher!", "REG_SZ");
var bKey =    WshShell.RegRead ("HKCUSoftwareACMEFortuneTeller");
WScript.Echo (WshShell.RegRead ("HKCUSoftwareACMEFortuneTellerMindReader"));
WshShell.RegDelete ("HKCUSoftwareACMEFortuneTellerMindReader");
WshShell.RegDelete ("HKCUSoftwareACMEFortuneTeller");
WshShell.RegDelete ("HKCUSoftwareACME");

 TABLAE相关(客户端动态增加行列）

function numberCells() {
    var count=0;
    for (i=0; i &lt; document.all.mytable.rows.length; i++) {
        for (j=0; j &lt; document.all.mytable.rows(i).cells.length; j++) {
            document.all.mytable.rows(i).cells(j).innerText = count;
            count++;
        }
    }
}

















１．身份证严格验证：

var aCity={11:"北京",12:"天津",13:"河北",14:"山西",15:"内蒙古",21:"辽宁",22:"吉林",23:" 黑龙江",31:"上海",32:"江苏",33:"浙江",34:"安徽",35:"福建",36:"江西",37:"山东",41:"河南",42: "湖北",43:"湖南",44:"广东",45:"广西",46:"海南",50:"重庆",51:"四川",52:"贵州",53:"云南",54: "西藏",61:"陕西",62:"甘肃",63:"青海",64:"宁夏",65:"新疆",71:"台湾",81:"香港",82:"澳门",91: "国外"}
  
function cidInfo(sId){
 var iSum=0
 var info=""
 if(!/^d{17}(d|x)$/i.test(sId))return false;
 sId=sId.replace(/x$/i,"a");
 if(aCity[parseInt(sId.substr(0,2))]==null)return "Error:非法地区";
 sBirthday=sId.substr(6,4)+"-"+Number(sId.substr(10,2))+"-"+Number(sId.substr(12,2));
 var d=new Date(sBirthday.replace(/-/g,"/"))
 if(sBirthday!=(d.getFullYear()+"-"+ (d.getMonth()+1) + "-" + d.getDate()))return "Error:非法生日";
 for(var i = 17;i&gt;=0;i --) iSum += (Math.pow(2,i) % 11) * parseInt(sId.charAt(17 - i),11)
 if(iSum%11!=1)return "Error:非法证号";
 return aCity[parseInt(sId.substr(0,2))]+","+sBirthday+","+(sId.substr(16,1)%2?"男":"女")
}
document.write(cidInfo("380524198002300016"),"");
document.write(cidInfo("340524198002300019"),"")
document.write(cidInfo("340524197711111111"),"")
document.write(cidInfo("34052419800101001x"),"");

 ２．验证ＩＰ地址

function isip(s){
 var check=function(v){try{return (v&lt;=255 &amp;&amp; v&gt;=0)}catch(x){return false}};
 var re=s.split(".")
 return (re.length==4)?(check(re[0]) &amp;&amp; check(re[1]) &amp;&amp; check(re[2]) &amp;&amp; check(re[3])):false
}
var s="202.197.78.129";
alert(isip(s))

 ３．加sp1后还能用的无边框窗口！！ 

/*--- Special Thanks For andot ---*/
/*
 This following code are designed and writen by Windy_sk 
 You can use it freely, but u must held all the copyright items!
*/
/*--- Thanks For andot Again ---*/
var CW_width = 400;
var CW_height = 300;
var CW_top = 100;
var CW_left = 100;
var CW_url = "/";
var New_CW = window.createPopup();
var CW_Body = New_CW.document.body;
var content = "";
var CSStext = "margin:1px;color:black; border:2px outset;border-style:expression_r(onmouseout=onmouseup=function(){this.style.borderStyle='outset'}, &#111;nmousedown=function(){if(event.button!=2)this.style.borderStyle='inset'});background-color:buttonface;width:16px;height:14px;font-size:12px;line-height:11px;cursor:Default;";
//Build Window
include.startDownload(CW_url, function(source){content=source});
function insert_content(){
 var temp = "";
 CW_Body.style.overflow  = "hidden";
 CW_Body.style.backgroundColor = "white";
 CW_Body.style.border  =  "solid black 1px";
 content = content.replace(/]*)&gt;/g,"");
 temp += "";
 temp += "";
 temp += "Chromeless Window For IE6 SP1";
 temp += "";
 temp += "?";
 temp += "0";
 temp += "1";
 temp += "x";
 temp += "";
 temp += "";
 temp += content;
 temp += "";
 temp += "";
 CW_Body.innerHTML = temp;
}
setTimeout("insert_content()",1000);
var if_max = true;
function show_CW(){
 window.moveTo(10000, 10000);
 if(if_max){
  New_CW.show(CW_top, CW_left, CW_width, CW_height);
  if(typeof(New_CW.document.all.include)!="undefined"){
   New_CW.document.all.include.style.width = CW_width;
   New_CW.document.all.Max.innerText = "1";
  }
  
 }else{
  New_CW.show(0, 0, screen.width, screen.height);
  New_CW.document.all.include.style.width = screen.width;
 }
}
window.onfocus  = show_CW;
window.onresize = show_CW;
// Move Window
var drag_x,drag_y,draging=false
function drag_move(e){
 if (draging){
  New_CW.show(e.screenX-drag_x, e.screenY-drag_y, CW_width, CW_height);
  return false;
 }
}
function drag_down(e){
 if(e.button==2)return;
 if(New_CW.document.body.offsetWidth==screen.width &amp;&amp; New_CW.document.body.offsetHeight==screen.height)return;
 drag_x=e.clientX;
 drag_y=e.clientY;
 draging=true;
 e.srcElement.setCapture();
}
function drag_up(e){
 draging=false;
 e.srcElement.releaseCapture();
 if(New_CW.document.body.offsetWidth==screen.width &amp;&amp; New_CW.document.body.offsetHeight==screen.height) return;
 CW_top  = e.screenX-drag_x;
 CW_left = e.screenY-drag_y;
}

电话号码的验证要求：　　(1)电话号码由数字、"("、")"和"-"构成　　(2)电话号码为3到8位　　(3)如果电话号码中包含有区号，那么区号为三位或四位　　(4)区号用"("、")"或"-"和其他部分隔开　　(5)移动电话号码为11或12位，如果为12位,那么第一位为0 　　(6)11位移动电话号码的第一位和第二位为"13" 　　(7)12位移动电话号码的第二位和第三位为"13" 　　根据这几条规则，可以与出以下正则表达式：　　(^[0-9]{3,4}-[0-9]{3,8}$)|(^[0-9]{3,8}$)|(^([0-9]{3,4})[0-9]{3,8}$)|(^0{0,1}13[0-9]{9}$)

function PhoneCheck(s) {
var str=s;
var reg=/(^[0-9]{3,4}-[0-9]{3,8}$)|(^[0-9]{3,8}$)|(^([0-9]{3,4})[0-9]{3,8}$)|(^0{0,1}13[0-9]{9}$)/
alert(reg.test(str));
}

  具有在输入非数字字符不回显的效果，即对非数字字符的输入不作反应。 function numbersonly(field,event){ var key,keychar; if(window.event){ key = window.event.keyCode; } else if (event){ key = event.which; } else{ return true } keychar = String.fromCharCode(key); if((key == null)||(key == 0)||(key == 8)||(key == 9)||(key == 13)||(key == 27)){ return true; } else if(("0123456789.").indexOf(keychar)&gt;-1){ window.status = ""; return true; } else { window.status = "Field excepts numbers only"; return false; } } 验证ip str=document.RegExpDemo.txtIP.value; if(/^(d{1,3}).(d{1,3}).(d{1,3}).(d{1,3})$/.test(str)==false) { window.alert('错误的IP地址格式'); document.RegExpDemo.txtIP.select(); document.RegExpDemo.txtIP.focus(); return; } if(RegExp.$1&lt;1 || RegExp.$1&gt;254||RegExp.$2&lt;0||RegExp.$2&gt;254||RegExp.$3&lt;0||RegExp.$3&gt;254||RegExp.$4&lt;1||RegExp.$4&gt;254) { window.alert('错误的IP地址'); document.RegExpDemo.txtIP.select(); document.RegExpDemo.txtIP.focus(); return; } //剔除 如 010.020.020.03 前面 的0 var str=str.replace(/0(d)/g,"$1"); str=str.replace(/0(d)/g,"$1"); window.alert(str); 							
		


