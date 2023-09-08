import torch
import torch.nn as nn
import numpy as np

class SelectorBlock(nn.Module):
    def __init__(self, input_size):
        super(SelectorBlock, self).__init__()        
        self.linear=nn.Linear(input_size,input_size)             
    def forward(self, x,x_2):                                  
        a=self.linear(x)           
        a=nn.ReLU()(a)                                                     
        s=torch.zeros_like(a)  
        s[a>0]=nn.Sigmoid()(a[a>0])
        x_1=x*s  
        x=x+x_1 
        x=x*x_2    
        explain=x_2+a                     
        return x,explain
class ResBlock(nn.Module):
    def __init__(self, input_size):
        super(ResBlock, self).__init__()
        self.linear=nn.Linear(input_size,input_size,dtype=torch.float32)                
        self.relu=nn.ReLU()        
    def forward(self, x):  
        a=x        
        x=self.linear(x)             
        x=self.relu(x)
        x=a+x           
        return x
    
class FusionAttentionBlock(nn.Module):
    def __init__(self, input_size):
        super(FusionAttentionBlock, self).__init__()
        self.q_linear=nn.Linear(input_size,input_size)  
        self.k_linear=nn.Linear(input_size,input_size)         
        self.v1_linear=nn.Linear(input_size,input_size)         
        self.v2_linear=nn.Linear(input_size,input_size)         
        self.bn=nn.BatchNorm1d(input_size)
        self.relu=nn.ReLU()
    def forward(self, x1,x2):      
        q=self.q_linear(x1)                     
        v1=q
        k=self.k_linear(x2)           
        v2=k
        attn=(q.transpose(-2, -1) @ k).softmax(dim=-1)
        v1=(v1 @ attn)
        v2=(v2 @ attn)

        v1=self.v1_linear(v1)                     
        v2=self.v2_linear(v2)                        
        x1=x1+v1
        x2=x2+v2    
        x1=self.bn(x1)          
        x2=self.bn(x2)
        return x1,x2

    

class Step(nn.Module):
    def __init__(self, input_size):
        super(Step, self).__init__()        
        self.resblock1=ResBlock(input_size)                
        self.resblock2=ResBlock(input_size)
        self.FAB=FusionAttentionBlock(input_size)
        self.selector=SelectorBlock(input_size)
        self.MLP=torch.nn.ModuleList()        
        self.MLP.append(ResBlock(input_size))        
        self.MLP.append(ResBlock(input_size))                
    def forward(self,input,a):      
        a=self.resblock2(a)
        a=nn.Sigmoid()(a)                
        x,explain=self.selector(input,a)
        x=self.resblock1(x)
        x_d,a=self.FAB(x,a)        
        for i in range(len(self.MLP)):
            x_d=self.MLP[i](x_d)                  
        return x_d,a,explain
class Head(nn.Module):
    def __init__(self, input_size,fusion_dim):
        super(Head, self).__init__() 
        self.downdim=nn.Linear(32,fusion_dim)
        self.final_linear=nn.Linear(input_size+fusion_dim,1)        
    def forward(self,input,a):
        a=self.downdim(a)
        a=nn.ReLU()(a)
        input=torch.concat((input,a),dim=-1)
        x=self.final_linear(input)                    
        x=nn.Sigmoid()(x)        
        return x
                       
class FusionSelectorNet(nn.Module):
    def __init__(self, input_size,fusion_dim=10,n_weight=2):        
        super(FusionSelectorNet, self).__init__()                
        self.init_step=Step(input_size)
        self.steps=torch.nn.ModuleList()
        for i in range(n_weight):
            self.steps.append(Step(input_size))                
        self.head=Head(input_size,fusion_dim)

                
    def forward(self,input,a):        
        
        x_a=torch.ones(input.shape).to(input.device)               
        x_a=self.init_step(input,x_a)[1]   
        res_list=[]
        for i in range(len(self.steps)):            
            x_d,x_a,w=self.steps[i](input,x_a)
            res_list.append(x_d)                                        
        res = torch.sum(torch.stack(res_list, dim=0), dim=0)                
        res=self.head(res,a)          
        return res
    def explain(self, input,a):
        x_a=torch.ones(input.shape).to(input.device)               
        x_a=self.init_step(input,x_a)[1]   
        res_list=[]
        explain = torch.zeros(input.shape).to(input.device)
        for i in range(len(self.steps)):            
            x_d,x_a,w=self.steps[i](input,x_a)
            res_list.append(x_d)  
            step_importance = torch.sum(x_d, dim=1)
            explain += torch.mul(w, step_importance.unsqueeze(dim=1))                                                                                      
        explain=nn.ReLU()(explain)  
        explain=explain.softmax(dim=-1)
        return explain        
    