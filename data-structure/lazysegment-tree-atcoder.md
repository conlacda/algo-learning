# Quick note
struct S {
    mint a; // a = tổng các element
    int size; // độ dài của sequence
};
struct F {
    mint a, b; // ax+b
};
S op(S l, S r) { return S{l.a + r.a, l.size + r.size}; } // hàm merge()
S e() { return S{0, 0}; } // a*x+size + 0*x+0 = a*x+size
S mapping(F l, S r) { return S{r.a * l.a + r.size * l.b, r.size}; }
F composition(F l, F r) { return F{r.a * l.a, r.b * l.a + l.b}; }
F id() { return F{1, 0}; } // x = 1*x+0 

/*
Update: ax+b -> F{a,b}
Mọi số đều có dạng ax+b
-> id() = F{1,0} => x = 1*x+0
struct S{a, size} => mọi phần tử đều có dạng a*x+size
op() là hàm tổng => S1+S2 = (a1x+b1) + (a2x+b) => (a1+a2)*x+(b1+b2)
    => S{a1+a2, b1+b2}
e() => op(x,e()) = x.  ax+size + 0.x+0 = ax+size() # hàm op() - hàm merge()
  
mapping()
Hình dung segment tree
        ----
    (5)--    --
   (1)--(4)  - - 
xét cục -- có sum = 5(bằng tổng của 2 cục bên dưới) và len=2
-> mapping Sum này với F(b,c) -> 5*b+2*c = S.sum*b+S.len*c
Lý giải: Mapping với F(b,c) -> 1*b+c+4*b+c = 5*b + 2*c = sum*b+len*c

Composition() - f∘g(x) = f(g(x))
g(x) = a1*x+b1
f∘g(x) = f(g(x)) = (a1*x+b1)*a2+b2
                 = (a1*a2)x + (b1*a2+b2) 
-> composition(F l, F r) = F {a1*a2, b1*a2+b2}
                            F{r.a * l.a, r.b * l.a + l.b};
*/
https://atcoder.github.io/ac-library/production/document_en/lazysegtree.html
