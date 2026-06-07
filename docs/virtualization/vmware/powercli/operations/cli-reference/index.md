# PowerCLI — CLI Reference

<div class="kb-summary">
Core PowerCLI cmdlets for VM management, host operations, cluster management, datastore/storage, vSAN, networking, snapshots, and tagging. All examples assume an active vCenter connection.
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
 
P
o
w
e
r
C
L
I
 
—
 
v
S
p
h
e
r
e
 
O
b
j
e
c
t
 
H
i
e
r
a
r
c
h
y
 
a
n
d
 
C
m
d
l
e
t
 
C
a
t
e
g
o
r
i
e
s
 
─
─
─
─
─
─
─
─
─
─
─
─
─
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
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
v
S
p
h
e
r
e
 
I
n
v
e
n
t
o
r
y
 
H
i
e
r
a
r
c
h
y
 
(
t
o
p
 
t
o
 
b
o
t
t
o
m
)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
v
C
e
n
t
e
r
 
-
>
 
D
a
t
a
c
e
n
t
e
r
 
-
>
 
C
l
u
s
t
e
r
 
-
>
 
E
S
X
i
 
H
o
s
t
 
-
>
 
V
M
 
/
 
R
e
s
o
u
r
c
e
 
P
o
o
l
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
v
C
e
n
t
e
r
 
-
>
 
D
a
t
a
c
e
n
t
e
r
 
-
>
 
D
a
t
a
s
t
o
r
e
 
/
 
N
e
t
w
o
r
k
 
-
>
 
V
M
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
U
s
e
 
-
L
o
c
a
t
i
o
n
 
t
o
 
s
c
o
p
e
:
 
G
e
t
-
V
M
 
-
L
o
c
a
t
i
o
n
 
(
G
e
t
-
C
l
u
s
t
e
r
 
"
P
r
o
d
"
)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
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
┐
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
C
o
m
p
u
t
e
 
C
m
d
l
e
t
s
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
 
G
e
t
-
V
M
 
/
 
S
e
t
-
V
M
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
N
e
w
-
V
M
 
/
 
R
e
m
o
v
e
-
V
M
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
S
t
a
r
t
/
S
t
o
p
/
R
e
s
t
a
r
t
-
V
M
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
 
 
 
M
o
v
e
-
V
M
 
(
v
M
o
t
i
o
n
)
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
 
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
 
/
 
S
e
t
-
V
M
H
o
s
t
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
                                                                                                        │
 
G
e
t
-
C
l
u
s
t
e
r
 
/
 
S
e
t
-
C
l
u
s
t
e
r
 
 
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
┐
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
S
t
o
r
a
g
e
 
C
m
d
l
e
t
s
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
G
e
t
-
D
a
t
a
s
t
o
r
e
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
G
e
t
-
H
a
r
d
D
i
s
k
 
/
 
S
e
t
-
H
a
r
d
D
i
s
k
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
G
e
t
-
S
n
a
p
s
h
o
t
 
/
 
N
e
w
-
S
n
a
p
s
h
o
t
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
R
e
m
o
v
e
-
S
n
a
p
s
h
o
t
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
G
e
t
-
V
s
a
n
D
i
s
k
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
G
e
t
-
V
s
a
n
C
l
u
s
t
e
r
H
e
a
l
t
h
S
u
m
m
a
r
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
┐
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
M
a
n
a
g
e
m
e
n
t
 
C
m
d
l
e
t
s
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
G
e
t
-
V
I
P
e
r
m
i
s
s
i
o
n
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
N
e
w
-
V
I
P
e
r
m
i
s
s
i
o
n
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
G
e
t
-
V
I
R
o
l
e
 
/
 
N
e
w
-
V
I
R
o
l
e
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
G
e
t
-
T
a
g
 
/
 
N
e
w
-
T
a
g
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
 
 
 
G
e
t
-
V
I
E
v
e
n
t
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
                                                                                                        │


                                                                                                        │
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │
 
 
 
 
 
 
G
e
t
-
V
i
e
w
 
(
r
a
w
 
A
P
I
)
 
 
 
 
 
 
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
 
m
a
n
a
g
e
m
e
n
t
 
w
o
r
k
s
t
a
t
i
o
n
 
o
r
 
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
 
s
e
r
v
e
r
 
r
u
n
n
i
n
g
 
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
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
N
e
t
w
o
r
k
 
p
a
t
h
:
 
j
u
m
p
 
h
o
s
t
 
-
>
 
H
T
T
P
S
/
4
4
3
 
-
>
 
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
 
-
>
 
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
 
e
n
d
p
o
i
n
t
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
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
 
 
P
i
p
e
l
i
n
e
 
 
 
 
 
 
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
 
p
i
p
e
;
 
G
e
t
-
V
M
 
|
 
G
e
t
-
S
n
a
p
s
h
o
t
 
c
h
a
i
n
s
 
c
m
d
l
e
t
s
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
W
h
e
r
e
-
O
b
j
e
c
t
 
 
=
 
f
i
l
t
e
r
 
i
t
e
m
s
 
i
n
 
a
 
p
i
p
e
l
i
n
e
 
b
y
 
p
r
o
p
e
r
t
y
 
v
a
l
u
e
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
S
e
l
e
c
t
-
O
b
j
e
c
t
 
=
 
c
h
o
o
s
e
 
w
h
i
c
h
 
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
 
t
o
 
d
i
s
p
l
a
y
 
o
r
 
e
x
p
o
r
t
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
F
o
r
E
a
c
h
-
O
b
j
e
c
t
 
=
 
i
t
e
r
a
t
e
 
o
v
e
r
 
e
a
c
h
 
i
t
e
m
 
i
n
 
t
h
e
 
p
i
p
e
l
i
n
e
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
E
x
p
o
r
t
-
C
s
v
 
 
 
 
=
 
w
r
i
t
e
 
p
i
p
e
l
i
n
e
 
o
u
t
p
u
t
 
t
o
 
C
S
V
 
f
i
l
e
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
                                                                                                        │


                                                                                                        │
 
 
F
o
r
m
a
t
-
T
a
b
l
e
 
 
=
 
r
e
n
d
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
 
a
s
 
c
o
l
u
m
n
s
 
i
n
 
t
h
e
 
c
o
n
s
o
l
e
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
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
<!-- diagram:powercli-operations -->

## VM Management

```powershell
# List all VMs
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB, VMHost | Sort-Object Name

# Filter by power state
Get-VM | Where-Object { $_.PowerState -eq 'PoweredOff' }

# Get VMs on a specific host
Get-VMHost -Name esxi01.example.com | Get-VM | Select-Object Name, PowerState

# Get VMs in a cluster
Get-Cluster -Name "Production" | Get-VM | Select-Object Name, VMHost, PowerState

# Power operations
Start-VM -VM (Get-VM -Name "web01")
Stop-VM -VM (Get-VM -Name "web01") -Confirm:$false
Restart-VM -VM (Get-VM -Name "web01") -Confirm:$false
Suspend-VM -VM (Get-VM -Name "web01") -Confirm:$false

# VM configuration
Set-VM -VM (Get-VM -Name "web01") -NumCpu 4 -MemoryGB 8 -Confirm:$false

# vMotion (live migration)
Move-VM -VM (Get-VM -Name "web01") -Destination (Get-VMHost -Name esxi02.example.com) -Confirm:$false
# Move to different datastore
Move-VM -VM (Get-VM -Name "web01") -Datastore (Get-Datastore -Name "vSAN-DS") -Confirm:$false
```

## Host Operations

```powershell
# List all hosts
Get-VMHost | Select-Object Name, ConnectionState, PowerState, Version, Parent | Sort-Object Name

# Host in a cluster
Get-Cluster -Name "Production" | Get-VMHost | Select-Object Name, CpuUsageMhz, MemoryUsageGB

# Host network adapters
Get-VMHost -Name esxi01.example.com | Get-VMHostNetworkAdapter | Select-Object Name, IP, SubnetMask, Mac

# Host services
Get-VMHost -Name esxi01.example.com | Get-VMHostService | Select-Object Key, Label, Running, Policy

# Enter/exit maintenance mode
Set-VMHost -VMHost (Get-VMHost -Name esxi01.example.com) -State Maintenance -Confirm:$false
Set-VMHost -VMHost (Get-VMHost -Name esxi01.example.com) -State Connected -Confirm:$false

# Host advanced settings
Get-VMHost -Name esxi01.example.com | Get-AdvancedSetting -Name "UserVars.SuppressShellWarning"
Get-VMHost -Name esxi01.example.com | Get-AdvancedSetting -Name "Net.TcpipHeapSize" | Set-AdvancedSetting -Value 32 -Confirm:$false
```

## Cluster Management

```powershell
# List clusters
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel, VsanEnabled | Format-Table -AutoSize

# HA configuration
Set-Cluster -Cluster (Get-Cluster -Name "Production") -HAEnabled $true -HAAdmissionControlEnabled $true -Confirm:$false

# DRS configuration
Set-Cluster -Cluster (Get-Cluster -Name "Production") -DrsEnabled $true -DrsAutomationLevel FullyAutomated -Confirm:$false

# Check DRS migration recommendations
Get-DrsRecommendation -Cluster (Get-Cluster -Name "Production") | Select-Object Reason, Target, Priority

# Apply all DRS recommendations
Get-DrsRecommendation -Cluster (Get-Cluster -Name "Production") | Apply-DrsRecommendation
```

## Datastore and Storage

```powershell
# List datastores
Get-Datastore | Select-Object Name, Type, CapacityGB, FreeSpaceGB, @{N="UsedPct";E={[math]::Round((1-$_.FreeSpaceGB/$_.CapacityGB)*100,1)}} | Sort-Object UsedPct -Descending

# Datastores below 20% free
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.20 }

# Datastore files (browse)
$ds = Get-Datastore -Name "vSAN-DS"
$browser = Get-View -Id $ds.ExtensionData.Browser
$spec = New-Object VMware.Vim.HostDatastoreBrowserSearchSpec

# Find VM with largest VMDK
Get-VM | ForEach-Object {
    Get-HardDisk -VM $_ | Select-Object @{N="VM";E={$_.Parent.Name}}, Name, CapacityGB
} | Sort-Object CapacityGB -Descending | Select-Object -First 20
```

## vSAN Operations

```powershell
# vSAN cluster health
Get-VsanClusterHealthSummary -Cluster (Get-Cluster -Name "vSAN-Cluster") | Select-Object OverallHealth

# Disk groups
Get-VsanDiskGroup -VMHost (Get-VMHost -Location (Get-Cluster -Name "vSAN-Cluster")) | Select-Object VMHost, @{N="CacheDisk";E={$_.ExtensionData.SsdUuid}}, @{N="CapacityDisks";E={$_.ExtensionData.NonSsd.Count}}

# vSAN disk health
Get-VsanDisk -VMHost (Get-VMHost -Location (Get-Cluster -Name "vSAN-Cluster")) | Select-Object CanonicalName, State, IsFlash | Format-Table -AutoSize

# vSAN objects
Get-VsanObject -Cluster (Get-Cluster -Name "vSAN-Cluster") | Where-Object { $_.HealthState -ne 'healthy' }
```

## Snapshots

```powershell
# Find all VMs with snapshots
Get-VM | Get-Snapshot | Select-Object VM, Name, Created, SizeMB, @{N="AgeDays";E={(Get-Date) - $_.Created | Select-Object -Expand TotalDays}} | Sort-Object AgeDays -Descending

# Find old snapshots (>7 days)
Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-7) }

# Create snapshot
New-Snapshot -VM (Get-VM -Name "web01") -Name "pre-patch-$(Get-Date -Format 'yyyyMMdd')" -Memory:$false -Quiesce:$false -Confirm:$false

# Remove a specific snapshot
Get-VM -Name "web01" | Get-Snapshot -Name "pre-patch-20260607" | Remove-Snapshot -RemoveChildren -Confirm:$false

# Remove all snapshots for a VM
Get-VM -Name "web01" | Get-Snapshot | Remove-Snapshot -RemoveChildren -Confirm:$false
```

## Tags and Custom Attributes

```powershell
# List all tag categories
Get-TagCategory | Select-Object Name, Description, Cardinality

# Create a tag
New-TagCategory -Name "Environment" -Cardinality Single -EntityType VirtualMachine
New-Tag -Name "Production" -Category (Get-TagCategory -Name "Environment")

# Assign a tag
Get-VM -Name "web01" | New-TagAssignment -Tag (Get-Tag -Name "Production")

# Find VMs with a tag
Get-VM | Where-Object { (Get-TagAssignment -Entity $_).Tag.Name -eq "Production" }

# Custom attributes
$vm = Get-VM -Name "web01"
$attr = Get-CustomAttribute -Name "Owner"
Set-Annotation -Entity $vm -CustomAttribute $attr -Value "john.doe@example.com"
```
