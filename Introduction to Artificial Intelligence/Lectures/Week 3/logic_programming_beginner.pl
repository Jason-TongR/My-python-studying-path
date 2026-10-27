% 人工智能导论 Week 3：Prolog / 逻辑程序设计新手讲义
% 建议：使用 SWI-Prolog 打开本文件，然后在 ?- 提示符逐条尝试下面注释中的查询。
% 注释行以 % 开头；查询要在 Prolog 提示符输入，不要把 ?- 一起写进本文件运行。
%
% 核心思想：描述“什么关系成立”，再提问；Prolog 负责按规则搜索答案。
% Kowalski 的概括是 Algorithm = Logic + Control：逻辑是事实和规则，
% 控制是如何使用它们。Prolog 主要用深度优先搜索和回溯来控制搜索。

% -----------------------------------------------------------------------------
% 1. 事实、规则和查询
% -----------------------------------------------------------------------------

% 事实：parent(父母, 孩子) 表示第一个人是第二个人的父母。
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
parent(pat, jim).

% 规则中的 :- 读作“如果”；逗号读作“并且”。
% X 是 Z 的祖父母，如果存在一个 Y，使得 X 是 Y 的父母且 Y 是 Z 的父母。
grandparent(X, Z) :-
    parent(X, Y),
    parent(Y, Z).

% 祖先关系有两种情况：
% 1) 直接父母是祖先（基础情况）；
% 2) 如果 X 是 Y 的父母，而 Y 是 Z 的祖先，那么 X 也是 Z 的祖先（递归情况）。
ancestor(X, Y) :-
    parent(X, Y).
ancestor(X, Z) :-
    parent(X, Y),
    ancestor(Y, Z).

% 试一试（在 SWI-Prolog 提示符输入）：
% ?- parent(tom, X).
% X = bob ;
% X = liz.
%
% ?- parent(X, ann).
% X = bob.
%
% ?- grandparent(tom, W).
% W = ann ;
% W = pat ;
% false.
%
% ?- ancestor(X, jim).
% X = pat ;
% X = tom ;
% X = bob ;
% false.
%
% 变量以大写字母或下划线开头。按 ; 请求下一个答案，false 表示没有更多答案。
% 查询中的变量是“想找什么”；Prolog 会尝试为变量找到合适的值。

% -----------------------------------------------------------------------------
% 2. Prolog 的基本写法：项、列表和关系
% -----------------------------------------------------------------------------

% 小写开头的名字通常是原子（常量），例如 tom、ann。
% 数字可以是整数或小数，例如 42、3.14。
% 变量以大写字母或 _ 开头，例如 X、People、_Rest。
% 复合项由名字和参数组成，例如 point(1, 2)，其名称/参数数目称为 point/2。
% 事实和规则都是 Horn 子句：一条规则有一个结论，右侧可以有多个条件。
% 规则中的变量通常按“对任意值”理解；查询中的变量则是在寻找“存在某个值”使查询成立。
% 程序的逻辑含义，是所有能从事实和规则推出的具体（无变量）关系。
%
% 列表是递归结构：[1,2,3] 等价于 [1|[2|[3|[]]]]。
% [Head|Tail] 把非空列表拆成首元素和剩余列表，例如：
% ?- [H|T] = [1,2,3].
% H = 1,
% T = [2,3].
%
% 注意：逻辑编程文献里 atom 常指“谓词应用”；Prolog 也用 atom 一词指 tom 这类原子常量。
% 看到具体上下文时，区分这两种用法。

% -----------------------------------------------------------------------------
% 3. 同一条列表关系的多种用法
% -----------------------------------------------------------------------------

% 为避免覆盖 SWI-Prolog 内置的 append/3，这里用 my_append/3 演示同一关系。
% my_append(左列表, 右列表, 连接结果)。
% 空列表接上 Ys，结果仍是 Ys。
my_append([], Ys, Ys).
% 非空列表 [X|Xs] 接上 Ys：结果以 X 开头，尾部是 Xs 接上 Ys 的结果。
my_append([X|Xs], Ys, [X|Zs]) :-
    my_append(Xs, Ys, Zs).

% 连接两个列表：
% ?- my_append([1,2], [3], L).
% L = [1,2,3].
%
% 反过来枚举 [1,2] 的所有拆分方式：
% ?- my_append(X, Y, [1,2]).
% X = [], Y = [1,2] ;
% X = [1], Y = [2] ;
% X = [1,2], Y = [] ;
% false.
%
% _ 是匿名变量，表示这个位置的值不关心。
% 第二个列表要求恰好只有一个元素，因此可找出原列表的最后一个元素：
% ?- my_append(_, [Last], [a,b,c]).
% Last = c ;
% false.
%
% 这就是关系式定义的力量：同一组规则可连接列表，也可反向拆分或匹配。

% -----------------------------------------------------------------------------
% 4. 统一、归结和回溯
% -----------------------------------------------------------------------------

% 统一（=）是让两个项匹配，并找出所需变量替换的过程：
% ?- f(X, b) = f(a, Y).
% X = a,
% Y = b.
%
% 复合项的名称、参数个数要相同，再逐个匹配参数：
% ?- point(X, X) = point(1, 2).
% false.                         % 同一个 X 不可能同时是 1 和 2
%
% ?- X = f(X).
% X = f(X).
% SWI-Prolog 默认不做 occurs check，因此允许这种无限项；需要严格检查时，
% 可用 unify_with_occurs_check/2。
%
% Prolog 从最左边的目标开始，按文件中子句的顺序逐条尝试。
% 匹配成功后继续证明规则右侧的条件；失败时回溯到最近的选择点，尝试下一条路。
% 查询得到答案后按 ;，就是让它从上次停下的选择点继续搜索。
%
% 规则顺序也会影响程序是否终止。下面这种写法把递归放在前面，可能一直递归，
% 以致后面的 parent/2 事实永远没有机会使用：
% bad_ancestor(X, Z) :- bad_ancestor(X, Y), parent(Y, Z).
% bad_ancestor(X, Y) :- parent(X, Y).
%
% SLD 归结在理论上是可靠且完备的：答案不会超出逻辑结论，所有逻辑结论也都在搜索树中。
% 但 Prolog 实际使用深度优先搜索；如果先进入无限分支，就可能永远到不了其他答案，
% 因而实际执行不一定完备。这是搜索顺序造成的限制。

% -----------------------------------------------------------------------------
% 5. 图搜索：避免在环路里兜圈
% -----------------------------------------------------------------------------

% 有向图的边。这里 a -> b -> c -> a 构成一个环。
edge(a, b).
edge(b, c).
edge(c, a).
edge(c, d).

% 简单路径：把已经走过的节点记下来，不允许再次进入已访问节点。
% path(起点, 终点, 路径)。
path(X, Y, Path) :-
    walk(X, Y, [X], ReversedPath),
    reverse(ReversedPath, Path).

% 到达目标时，已访问列表就是反向路径。
walk(X, X, Visited, Visited).
walk(X, Y, Visited, Path) :-
    edge(X, Z),
    \+ member(Z, Visited),
    walk(Z, Y, [Z|Visited], Path).

% ?- path(a, d, P).
% P = [a,b,c,d] ;
% false.
%
% ?- path(a, e, P).
% false.
%
% \+ Goal 是“否定即失败”：当 Goal 无法被证明时，它成功。
% 这里用它阻止路径重复访问节点。若直接递归找路径而不记录访问过的节点，
% 图中有环时可能无限搜索，甚至对不存在的路径也无法给出 false。

% -----------------------------------------------------------------------------
% 6. 水壶问题：状态转移和迭代加深
% -----------------------------------------------------------------------------

% 状态 jugs(X,Y)：5 升壶有 X 升，3 升壶有 Y 升。
% move(当前状态, 操作名称, 操作后的状态)。
move(jugs(_, Y), fill1, jugs(5, Y)).
move(jugs(X, _), fill2, jugs(X, 3)).
move(jugs(_, Y), empty1, jugs(0, Y)).
move(jugs(X, _), empty2, jugs(X, 0)).
move(jugs(X, Y), pour12, jugs(X1, Y1)) :-
    Amount is min(X, 3 - Y),
    X1 is X - Amount,
    Y1 is Y + Amount.
move(jugs(X, Y), pour21, jugs(X1, Y1)) :-
    Amount is min(Y, 5 - X),
    X1 is X + Amount,
    Y1 is Y - Amount.

% 目标：任意一个壶里恰有 4 升。
goal(jugs(4, _)).
goal(jugs(_, 4)).

% 普通深度优先搜索。对有环的状态空间，它可能沿着很长的路径一直搜索。
solve(State, []) :-
    goal(State).
solve(State, [Action|Actions]) :-
    move(State, Action, NextState),
    solve(NextState, Actions).

% 迭代加深：length/2 依次生成长度为 0、1、2……的动作列表，
% 每次只搜索一个固定深度，因此第一次找到的解是最短解之一。
solve_id(State, Actions) :-
    length(Actions, _),
    solve(State, Actions).

% ?- solve_id(jugs(0,0), Actions).
% Actions = [fill1,pour12,empty2,pour12,fill1,pour12] ;
% ...
%
% is 用于计算已经确定的算术表达式；后面的 CLP(FD) 部分会展示可反向推理的约束算术。

% -----------------------------------------------------------------------------
% 7. 约束逻辑编程：N 皇后
% -----------------------------------------------------------------------------

% CLP(FD) 是有限域整数约束库。变量可先有取值范围，再用约束缩小范围。
% #=、#\=、#<、#> 是约束算术符号，不是普通的立即计算。
:- use_module(library(clpfd)).

% 先生成再检查的版本：列出 1..N 的所有行排列，再检查对角线。
% permutation/2 会产生 N! 个候选，N 增大后会很慢。
queens_generate_test(N, Rows) :-
    numlist(1, N, AvailableRows),
    permutation(AvailableRows, Rows),
    safe_plain(Rows).

safe_plain([]).
safe_plain([Queen|Others]) :-
    no_attack_plain(Queen, Others, 1),
    safe_plain(Others).

no_attack_plain(_, [], _).
no_attack_plain(Queen, [Other|Others], Distance) :-
    Queen =\= Other + Distance,
    Queen =\= Other - Distance,
    NextDistance is Distance + 1,
    no_attack_plain(Queen, Others, NextDistance).

% queens(N, Rows)：第 i 列皇后所在的行号是 Rows 的第 i 个元素。
queens(N, Rows) :-
    length(Rows, N),
    Rows ins 1..N,
    safe_queens(Rows),
    labeling([ff], Rows).

% 检查皇后之间没有同列、同对角线冲突。
safe_queens([]).
safe_queens([Queen|Others]) :-
    no_attack(Queen, Others, 1),
    safe_queens(Others).

no_attack(_, [], _).
no_attack(Queen, [Other|Others], Distance) :-
    Queen #\= Other,
    abs(Queen - Other) #\= Distance,
    NextDistance is Distance + 1,
    no_attack(Queen, Others, NextDistance).

% labeling/2 才开始实际尝试变量取值；[ff] 使用“最少可选值优先”的变量选择策略。
% ?- queens(8, Rows).
% Rows = [...].
%
% 对比运行：?- queens_generate_test(8, Rows). 和 ?- queens(8, Rows).
% 约束传播能在搜索前排除许多不可能的取值，规模增大时通常快得多。

% -----------------------------------------------------------------------------
% 8. SEND + MORE = MONEY：约束算术
% -----------------------------------------------------------------------------

send_more_money([S,E,N,D,M,O,R,Y]) :-
    Vars = [S,E,N,D,M,O,R,Y],
    Vars ins 0..9,
    all_different(Vars),
    S #\= 0,
    M #\= 0,
    1000*S + 100*E + 10*N + D
      + 1000*M + 100*O + 10*R + E
      #= 10000*M + 1000*O + 100*N + 10*E + Y,
    labeling([], Vars).

% ?- send_more_money(Digits).
% Digits = [9,5,6,7,1,0,8,2] ;
% false.
% 即 9567 + 1085 = 10652。每个字母是不同数字，首位 S 和 M 不能为 0。
% 不需要自己写搜索循环：声明约束，再由 labeling/2 搜索。

% -----------------------------------------------------------------------------
% 9. 数独：用约束描述规则
% -----------------------------------------------------------------------------

% Rows 是 9x9 的列表矩阵。题目已知数字直接填整数，空格填变量。
% 本谓词约束每行、每列和每个 3x3 宫的数字各不相同，然后搜索答案。
sudoku(Rows) :-
    length(Rows, 9),
    maplist(same_length(Rows), Rows),
    append(Rows, Cells),
    Cells ins 1..9,
    maplist(all_distinct, Rows),
    transpose(Rows, Columns),
    maplist(all_distinct, Columns),
    Rows = [R1,R2,R3,R4,R5,R6,R7,R8,R9],
    boxes(R1, R2, R3),
    boxes(R4, R5, R6),
    boxes(R7, R8, R9),
    maplist(label, Rows).

% 每次取连续三格，共取三行，组成一个 3x3 宫。
boxes([], [], []).
boxes([A1,A2,A3|As], [B1,B2,B3|Bs], [C1,C2,C3|Cs]) :-
    all_distinct([A1,A2,A3,B1,B2,B3,C1,C2,C3]),
    boxes(As, Bs, Cs).

% 可直接尝试的查询。每个 _ 都是独立的空格变量：
% ?- Puzzle = [
%      [5,3,_,_,7,_,_,_,_], [6,_,_,1,9,5,_,_,_], [_,9,8,_,_,_,_,6,_],
%      [8,_,_,_,6,_,_,_,3], [4,_,_,8,_,3,_,_,1], [7,_,_,_,2,_,_,_,6],
%      [_,6,_,_,_,_,2,8,_], [_,_,_,4,1,9,_,_,5], [_,_,_,_,8,_,_,7,9]
%    ], sudoku(Puzzle).
% 课件重点是建模方式：只描述行、列、宫的规则，交给约束传播和搜索求解。

% -----------------------------------------------------------------------------
% 10. 约束让关系可以反向查询：阶乘
% -----------------------------------------------------------------------------

% n_factorial(N,F) 表示 N 的阶乘是 F。
% 用 #= 而不是 is，所以关系可在一定条件下反向使用。
n_factorial(0, 1).
n_factorial(N, F) :-
    N #> 0,
    PreviousN #= N - 1,
    F #= N * PreviousF,
    n_factorial(PreviousN, PreviousF).

% ?- n_factorial(5, F).
% F = 120.
%
% ?- n_factorial(N, 120).
% N = 5.
%
% 注意：递归关系要有足够约束才能让搜索收敛；变量完全未受限制时，递归查询可能无限搜索。

% -----------------------------------------------------------------------------
% 总结与练习方向
% -----------------------------------------------------------------------------

% 1. 逻辑程序用事实和规则描述关系；查询要求 Prolog 找出成立的变量取值。
% 2. 统一让项匹配；归结选择规则来证明目标；失败时通过回溯尝试其他分支。
% 3. 深度优先搜索的顺序会影响效率和终止性；递归规则的顺序尤其重要。
% 4. 搜索问题可建模为状态、动作和目标；迭代加深可寻找最短解。
% 5. CLP(FD) 先传播约束，再进行搜索，适合 N 皇后、字母算术和数独。
%
% 课件实验建议：家庭关系、append/3、最短水壶解、约束 N 皇后、SEND + MORE = MONEY、数独。
% 下一讲转向局部搜索：只关注最终状态，用爬山、模拟退火或遗传算法逐步改进。
