# 定义 rank 函数：输入集合 A 和全集元素个数 n，返回 A 在这里采用的二进制/字典序编号。
def rank(A:set,n:int) -> int:
    # 按字典序/二进制位权计算集合 A 的编号；输入 A 中的元素应处于 0 到 n-1。

    # 从编号 0 开始累加，之后每个元素 i 都对应权重 2 的 i 次方。
    r:int =0

    # 检查从 0 到 n-1 的每一个可能元素，决定对应二进制位是否置 1。
    for i in reversed(range(n)):
        # 若 i 在集合 A 中，布尔值 True 会按整数 1 参与计算；否则按 0 计算。
        r = 2*r + (i in A)

    # 返回所有已设置二进制位的权重之和，即集合的唯一整数编码。
    return r

    # 后置条件：返回值 r 是整数，且每个 i∈A 对应二进制位权重 2**i。
    """
    post: r = int(X(A))
    """

    def unrank(r:int,n:int) -> set :
        
        """
        an implemetation of the unrank algorithm
        """

        """
        per : r: [0:2^n]
        """

        A =set()

        for a in range(n):

            if r%2 == 1 :
                A = A | {a}

            r //= 2

        return A
        """
        post : int(X(A)) = r
        """

        def successor(A:set,n:int) -> set :
            """
            an implementation of the successor algorithm
            """
            """
            pre: A: 2^[0:n)
            """
            B, a = A, 0

            while(a in B):

                B,a = B-{a},a+1

            if a < n:

                B = B | {a}

            return B
            """
            post : X(B) = X(A) + 1
            """