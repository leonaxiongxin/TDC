TDC = readNPY('..\TDC\IS-QBXB-13-17.npy');
[n,~]=size(TDC);
X=zeros(n,1);
for i=1:n
    X(i)=i;
end
scatter(X,TDC,'.');