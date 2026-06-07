# VMware PowerCLI

<div class="kb-summary">
PowerCLI is VMware's official PowerShell module suite for automating and managing vSphere, NSX, vSAN, vCD, and other VMware products. It provides 900+ cmdlets covering the full vSphere API, enabling scripted VM operations, host configuration, storage management, and reporting at scale.
</div>

```text
┌
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
 
V
M
w
a
r
e
 
P
o
w
e
r
C
L
I
 
O
v
e
r
v
i
e
w
 
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┐


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
┌
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┐
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
V
M
w
a
r
e
 
P
o
w
e
r
C
L
I
 
—
 
P
o
w
e
r
S
h
e
l
l
 
m
o
d
u
l
e
 
s
u
i
t
e
 
f
o
r
 
v
S
p
h
e
r
e
 
a
u
t
o
m
a
t
i
o
n
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
B
u
i
l
t
 
o
n
 
t
o
p
 
o
f
 
t
h
e
 
v
S
p
h
e
r
e
 
S
O
A
P
/
R
E
S
T
 
A
P
I
s
 
—
 
s
a
m
e
 
c
a
l
l
s
 
a
s
 
v
C
e
n
t
e
r
 
U
I
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
P
l
a
t
f
o
r
m
:
 
P
o
w
e
r
S
h
e
l
l
 
7
+
 
(
c
r
o
s
s
-
p
l
a
t
f
o
r
m
)
 
o
r
 
W
i
n
d
o
w
s
 
P
o
w
e
r
S
h
e
l
l
 
5
.
1
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
I
n
s
t
a
l
l
:
 
I
n
s
t
a
l
l
-
M
o
d
u
l
e
 
V
M
w
a
r
e
.
P
o
w
e
r
C
L
I
 
f
r
o
m
 
P
S
G
a
l
l
e
r
y
;
 
4
0
+
 
s
u
b
-
m
o
d
u
l
e
s
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
S
e
s
s
i
o
n
:
 
C
o
n
n
e
c
t
-
V
I
S
e
r
v
e
r
 
-
>
 
$
g
l
o
b
a
l
:
D
e
f
a
u
l
t
V
I
S
e
r
v
e
r
 
-
>
 
a
l
l
 
c
m
d
l
e
t
s
 
u
s
e
 
i
t
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
└
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┘
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
┌
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┐
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
C
o
r
e
 
M
o
d
u
l
e
s
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
V
i
m
A
u
t
o
m
a
t
i
o
n
.
C
o
r
e
 
 
V
M
 
+
 
h
o
s
t
 
+
 
c
l
u
s
t
e
r
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
V
i
m
A
u
t
o
m
a
t
i
o
n
.
V
d
s
 
 
 
v
D
S
 
+
 
p
o
r
t
g
r
o
u
p
s
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
V
i
m
A
u
t
o
m
a
t
i
o
n
.
S
t
o
r
a
g
e
 
 
V
M
D
K
 
+
 
d
a
t
a
s
t
o
r
e
s
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
V
i
m
A
u
t
o
m
a
t
i
o
n
.
N
s
x
t
 
 
N
S
X
-
T
 
p
o
l
i
c
y
 
o
b
j
e
c
t
s
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
└
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┘
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
┌
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┐
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
A
d
d
-
o
n
 
M
o
d
u
l
e
s
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
V
i
m
A
u
t
o
m
a
t
i
o
n
.
S
r
m
 
 
 
S
R
M
 
r
e
c
o
v
e
r
y
 
p
l
a
n
s
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
V
i
m
A
u
t
o
m
a
t
i
o
n
.
H
c
x
 
 
 
H
C
X
 
m
i
g
r
a
t
i
o
n
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
V
i
m
A
u
t
o
m
a
t
i
o
n
.
H
o
r
i
z
o
n
 
 
H
o
r
i
z
o
n
 
V
D
I
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
V
i
m
A
u
t
o
m
a
t
i
o
n
.
v
R
O
p
s
 
 
A
r
i
a
 
O
p
e
r
a
t
i
o
n
s
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
└
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┘
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
┌
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┐
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
C
o
n
n
e
c
t
i
o
n
 
M
o
d
e
l
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
C
o
n
n
e
c
t
-
V
I
S
e
r
v
e
r
 
-
S
e
r
v
e
r
 
<
F
Q
D
N
>
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
-
>
 
S
S
O
 
t
o
k
e
n
 
f
r
o
m
 
v
C
e
n
t
e
r
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
-
>
 
$
g
l
o
b
a
l
:
D
e
f
a
u
l
t
V
I
S
e
r
v
e
r
 
s
e
t
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
-
>
 
A
l
l
 
c
m
d
l
e
t
s
 
u
s
e
 
t
h
i
s
 
i
m
p
l
i
c
i
t
l
y
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
└
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┘
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
┌
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┐
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
A
P
I
 
B
i
n
d
i
n
g
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
H
i
g
h
-
l
e
v
e
l
:
 
G
e
t
-
V
M
 
-
>
 
V
I
 
o
b
j
e
c
t
s
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
L
o
w
-
l
e
v
e
l
:
 
G
e
t
-
V
i
e
w
 
-
>
 
r
a
w
 
v
S
p
h
e
r
e
 
A
P
I
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
V
i
e
w
 
o
b
j
e
c
t
s
:
 
f
a
s
t
e
r
,
 
n
o
 
w
r
a
p
p
e
r
s
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
E
x
t
e
n
s
i
o
n
D
a
t
a
:
 
.
N
E
T
 
S
D
K
 
a
c
c
e
s
s
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
└
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
─
┘
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
P
h
y
s
i
c
a
l
 
I
n
f
r
a
s
t
r
u
c
t
u
r
e
:
 
W
i
n
d
o
w
s
/
L
i
n
u
x
 
j
u
m
p
 
h
o
s
t
 
w
i
t
h
 
P
o
w
e
r
S
h
e
l
l
 
7
+
 
i
n
s
t
a
l
l
e
d
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
N
e
t
w
o
r
k
:
 
H
T
T
P
S
/
4
4
3
 
t
o
 
v
C
e
n
t
e
r
 
F
Q
D
N
 
 
·
 
 
D
N
S
 
r
e
s
o
l
u
t
i
o
n
 
r
e
q
u
i
r
e
d
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
K
e
y
 
t
e
r
m
s
:
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
V
I
 
O
b
j
e
c
t
 
 
 
 
=
 
h
i
g
h
-
l
e
v
e
l
 
w
r
a
p
p
e
r
 
(
G
e
t
-
V
M
,
 
G
e
t
-
V
M
H
o
s
t
)
 
w
i
t
h
 
h
e
l
p
e
r
 
p
r
o
p
e
r
t
i
e
s
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
V
i
e
w
 
O
b
j
e
c
t
 
 
=
 
r
a
w
 
v
S
p
h
e
r
e
 
A
P
I
 
o
b
j
e
c
t
;
 
f
a
s
t
e
r
 
b
u
t
 
n
o
 
h
e
l
p
e
r
 
p
r
o
p
e
r
t
i
e
s
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
S
O
A
P
 
A
P
I
 
 
 
 
 
=
 
v
S
p
h
e
r
e
 
l
e
g
a
c
y
 
A
P
I
 
(
p
o
r
t
 
4
4
3
 
/
s
d
k
)
;
 
u
s
e
d
 
b
y
 
m
o
s
t
 
c
m
d
l
e
t
s
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
R
E
S
T
 
A
P
I
 
 
 
 
 
=
 
v
S
p
h
e
r
e
 
m
o
d
e
r
n
 
A
P
I
;
 
u
s
e
d
 
b
y
 
n
e
w
e
r
 
N
S
X
/
v
S
A
N
 
c
m
d
l
e
t
s
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
S
S
O
 
T
o
k
e
n
 
 
 
 
=
 
s
e
s
s
i
o
n
 
c
r
e
d
e
n
t
i
a
l
;
 
v
a
l
i
d
 
8
 
h
 
b
y
 
d
e
f
a
u
l
t
;
 
a
u
t
o
-
r
e
n
e
w
e
d
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
P
S
G
a
l
l
e
r
y
 
 
 
 
=
 
P
o
w
e
r
S
h
e
l
l
 
m
o
d
u
l
e
 
r
e
p
o
s
i
t
o
r
y
;
 
s
o
u
r
c
e
 
f
o
r
 
I
n
s
t
a
l
l
-
M
o
d
u
l
e
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
D
e
f
a
u
l
t
V
I
S
e
r
v
e
r
 
=
 
i
m
p
l
i
c
i
t
 
c
o
n
n
e
c
t
i
o
n
 
t
a
r
g
e
t
 
f
o
r
 
a
l
l
 
c
m
d
l
e
t
s
 
i
n
 
s
e
s
s
i
o
n
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


+
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
+
```
<!-- diagram:powercli -->

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How PowerCLI connects to vCenter/ESXi, module structure, credential handling, and integration points.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installing PowerCLI, connecting to vCenter, service account setup, and multi-vCenter environments.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Cmdlet reference, scripts library, health checks, procedures, lifecycle, and automation patterns.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Service account least privilege, credential storage, certificate validation, and connection hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Connection errors, cmdlet failures, certificate issues, and API permission errors.</span>
</a>

</div>
