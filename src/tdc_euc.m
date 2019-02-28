% % %  
% % % %  tic;
RTA=0:0.1:9999.9;
RTM=reshape(RTA,100,1000);
disp(RTM(100,1000));

% % RTM=[1,1,0,2,1,1;1,1,0,2,1,1;1,1,1,1,1,1];
TRM=RTM';
%将术语文献矩阵（RTM）转化为相似矩阵（TTM）
[n,~]=size(TRM);
X=1-pdist(TRM,'cosine');
% m = 1;
% X=load('X_5y.dat');
TTM=squareform(X);
for i=1:n
    TTM(i,i)=1;
end
% % TTM=load('TTM_5y.dat');
% % 计算TTM中心
Center=mean(TTM);
DS=zeros(1,n);
 c=1.3;  %c等于1.3时最稳定
%求Dist、DS
for i=1:n
    DS(1,i)=1/(c^(norm(TTM(i,:)-Center)));
end
Density=sum(DS)/n; %Density
disp(Density)
% 计算抽取一行一列后的SD
T_DS=zeros(1,n-1);
T_Density=zeros(n,1);
for i=1:n
    if mod(i,100)==0
        disp(i);
    end
    T_TTM=TTM;
    T_TTM(:,i)=[];
    T_TTM(i,:)=[];
    T_Center=mean(T_TTM);
    for j=1:n-1
        T_DS(1,j)=1/(c^(norm(T_TTM(j,:)-T_Center)));
    end
    T_Density(i)=sum(T_DS)/(n-1);
end
AVG_SD=sum(abs(T_Density-Density))/n;
TDC=(T_Density-Density)/AVG_SD; 
% toc;   
% t=toc;
csvwrite('matlab_test.dat',TDC); 
% csvwrite('IS-QBXB.dat',Density);
% csvwrite('IS-QBXB.dat',T_Density);

