def tatsuo2(YL1,YL2,YL3,EP1,EP2,EP3,W,WS,NYA,NYB,NY,NX,NS):
    import numpy as np
    size =10000
    A=np.zeros((size,size),dtype='float')
    B=np.zeros((size,size),dtype='float')
    Y=np.zeros(size)
    KA=np.zeros(size,dtype='int')
    KB=np.zeros(size,dtype='int')
    KN=np.zeros(size,dtype='int')
    X=np.zeros(size,dtype='float')
    R=np.zeros(size,dtype='float')
    MORDER=0
    NORDER=0
    C=0.0
    DY1=YL1/float(NYA)
    DY2=YL2/float(NYB-NYA)
    DY3=YL3/float(NY-NYB)
    DX1=(W - WS)/float(NX-NS)
    DX2=WS/float(NS)
    NX1=NX+1
    NY1=NY+1
    NS1=NS+1
    MORDER=NX1*NY1 #Inicialization
    for I in range(1,MORDER+1):
        KA[I]=1      
    for I in range(1,NX1+1):    #Top and botton conductors
        KA[I]=0
        KA[NY*NX1+I]=0
    for I in range(1,NY1+1):   #Left side conductor
        KA[(I-1)*NX1+1]=0
    for I in range(1,NS1+1):     #Metal strip
        IJ=NYA*NX1+NX-NS+I
        KA[IJ] = 2
    ICOUNT=0         # Evaluate KB holds unknown nodes only
    for I in range(1,MORDER+1):
        if KA[I] == 1:
            ICOUNT = ICOUNT +1
            KB[ICOUNT]=I
    NORDER=ICOUNT
    # Calculate KN, known nonzero potential nodes
    ICN=0
    for I in range(1,MORDER+1):
        if KA[I]==2:
            ICN+=1
            KN[ICN]=I
    #Set matrix order (=number of nodes) as:
    for I in range(1,NY+1):
        E=EP1
        if (I>NYA)and(I<= NYB):
            E=EP2
        if I > NYB :
            E=EP3
        #Set vertical element dimension
        DY=DY1
        if I > NYA:
            DY=DY2
        if I > NYB:
            DY=DY3
        for J in range(1,NX+1):
            DX=DX1
            if J>(NX-NS):
                DX=DX2
            DXBYDY = E*DX/DY
            DYBYDX = E*DY/DX
            DXYD = DXBYDY + DYBYDX
            K1 =(NX+1)*I + J +1
            K2 = K1 - ( NX+1)
            K3= K2-1
            K4= K1-1
            A[K4,K4]=A[K4,K4]+DXBYDY
            A[K3,K3]=A[K3,K3]+DXYD
            A[K2,K2]=A[K2,K2]+DYBYDX
            A[K3,K2]=A[K3,K2]-DYBYDX
            A[K3,K4]=A[K3,K4]-DXBYDY
            A[K2,K3]=A[K2,K3]-DYBYDX
            A[K4,K3]=A[K4,K3]-DXBYDY

            A[K4,K4]=A[K4,K4]+DYBYDX
            A[K1,K1]=A[K1,K1]+DXYD
            A[K2,K2]=A[K2,K2]+DXBYDY
            A[K4,K1]=A[K4,K1]-DYBYDX
            A[K2,K1] =A[K2,K1]-DXBYDY
            A[K1,K4]=A[K1,K4]-DYBYDX
            A[K1,K2]=A[K1,K2]-DXBYDY
        # print(A)
    for I in range(1,NORDER+1):
        for J in range(1,NORDER+1):
            IN = KB[I]
            JN=KB[J]
            B[I,J]=A[IN,JN]
    #Generate R from known potentials
    for I in range(1,NORDER+1):
        IX=KB[I]
        R[I]=0.0
        for J in range(1,NS1+1):
            IY=KN[J]
            R[I]=R[I]-A[IX,IY] 
    for K in range(1,NORDER+1):
        if B[K,K]<= 0:
            print ('error en choleski')
            print(K)
            print(B[K,K])
        else:
            B[K,K]=np.sqrt(B[K,K])
            KP1=K+1
            if KP1>NORDER:
                pass
            else:
                for I in range(KP1,NORDER+1):
                    B[K,I]=B[K,I]/B[K,K]
                for I in range(KP1,NORDER+1):
                    for J in range(I,NORDER+1):
                         B[I,J] = B[I,J]-B[K,I]*B[K,J]
    # First perform forward substitution to solve for Y. Solve LY=R
    # print(Y[1],R[1],B[1,1])
    Y[1] = R[1]/B[1,1]
    for K in range(2,NORDER+1):
        SUM=R[K]
        KM1=K-1
        for J in range(1,KM1+1):
            SUM-=B[J,K]*Y[J]
        Y[K]=SUM/B[K,K]
    #Now back substitution to calculate X
    # Solve UX=Y
    X[NORDER]=Y[NORDER]/B[NORDER,NORDER]
    for J in range(2,NORDER+1):
        NJ1= NORDER -J+1
        JM1=J-1
        SUM=Y[NJ1]
        for K in range(1,JM1+1):
            NK1=NORDER-K+1
            SUM-=X[NK1]*B[NJ1,NK1]
        X[NJ1]=SUM/B[NJ1,NJ1]
    #R is reused for nodal potentials
    for I in range(1,MORDER+1):
        R[I]=0.0
    #Calculate potentials
    for I in range(1,NORDER+1):
        IJ=KB[I]
        R[IJ]=X[I]
    #Known nonzero potentials
    for I in range(1,NS1+1):
        IJ=KN[I]
        R[IJ]=1.0
    #print(R)
    #Calculate capacitance
    for I in range(1,MORDER+1):
        for J in range(1,MORDER+1):
            C=C+R[I]*A[I,J]*R[J]
    # print('Capacitance')
    return C
def tatsuo(YL1,YL2,YL3,EP1,EP2,EP3,W,WS,NYA,NYB,NY,NX,NS):
    import numpy as np
    C0=tatsuo2(YL1,YL2,YL3,EP1,EP2,EP3,W,WS,NYA,NYB,NY,NX,NS)
    C1=tatsuo2(YL1,YL2,YL3,1,1,1,W,WS,NYA,NYB,NY,NX,NS)
    vp=3e8/np.sqrt(C1/C0)
    Z0=120*np.pi/C0
    Z1=Z0*np.sqrt(C0/C1)
    return C0,C1,Z0,Z1,vp
