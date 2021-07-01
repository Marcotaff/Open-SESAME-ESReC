soc=[0
25
50
75
100];
% SoCs at which resistance data is available
temp=[-20,0,20,40]; % Temperatures at which resistance data is available
[soc,temp]=meshgrid(soc,temp);
data=[0.094602697	0.048132397	0.036161367	0.028086448
0.08865539	0.037587896	0.026150316	0.02340783
0.087310664	0.036228646	0.02533813	0.022996474
0.08802861	0.036457714	0.025311174	0.022937149
0.094094329	0.044707868	0.027517088	0.023973051
]; % resistance data
data=data';
[soc1,temp1]=meshgrid([0:100],[-20:40]);
z=griddata(soc,temp,data,soc1,temp1);
surf(soc1,temp1,z)