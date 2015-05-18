# Defcon Quals 2015 - Access Control

## Category: Reverse
## Points: 1

本次Defcon Quals看的最透彻的题了，给出的client与server交互遵循一个协议。client中初始的用户名是grumpy，运行一次以后list出了服务器上的一些用户名，grumpy没有print key的权限，可以猜测下面的用户里面一定有一个拥有print key的权限。

```
mrvito
gynophage
selir
jymbolia
sirgoon
duchess
deadwood
```

print key执行后还有个challenge，加密的算法都是异或。

最直接的方法，看清楚password的算法自己重写client，不过需要coding的比较多。我想的直接使用patch的方法，在gdb里面改掉用户名，这里给的用户名的存储空间好短，不过没事直接写进去就行，覆盖就覆盖了。

使用的gdb脚本如下

```
file client
set args 54.84.39.118 
b *0x804893e
b *0x804896b
b *0x8048bb9
r
set {char}0x8049164=100
set {char}0x8049165=117
set {char}0x8049166=99
set {char}0x8049167=104
set {char}0x8049168=101
set {char}0x8049169=115
set {char}0x804916a=115
set {char}0x804916b=10
set {char}0x804916c=0
c
set {char}0x804916c=100
set {char}0x804916d=117
set {char}0x804916e=99
set {char}0x804916f=104
set {char}0x8049170=101
set {char}0x8049171=115
set {char}0x8049172=115
set {char}0x8049173=0
set {int}0x804b468=3
c
set $eip=0x8048bcd
c
```

一共三个断点，一个在发送用户名的时候最后要加个\n，一个在计算密码的时候（这俩居然用的不是同一个字符串），顺带把一个state变量也改了让它进入print key的流程。最后一个断点在进入challenge的if之前，我不知道为啥它卡在那了，就直接改了eip让它进去。执行gdb就得到了flag，不过已经是比赛之后啦。

```
Breakpoint 1 at 0x804893e
Breakpoint 2 at 0x804896b
Breakpoint 3 at 0x8048bb9
Socket created
Enter message : hack the world
<< connection ID: RvNvOnh5F~z2nx


*** Welcome to the ACME data retrieval service ***
what version is your client?

<< hello...who is this?

Breakpoint 1, 0x0804893e in ?? ()

Breakpoint 2, 0x0804896b in ?? ()
<<

<< enter user password

<< hello duchess, what would you like to do?

<< grumpy

Breakpoint 3, 0x08048bb9 in ?? ()
<<
mrvito
gynophage
selir
jymbolia
sirgoon
duchess
deadwood
hello duchess, what would you like to do?

<< challenge: ,@%6?
answer?

<< the key is: The only easy day was yesterday. 44564


<< hello duchess, what would you like to do?
```
