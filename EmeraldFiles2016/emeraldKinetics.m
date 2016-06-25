
%Rate Constants
k1=10e5; %M^-1  s^-1
k2=1.2; %s^-1
k2r=1e7;% M^-1  s^-1
k3=10e4; %M^-1  s^-1
k4=1e4; %M^-1  s^-1
k5=1e7; %M^-1  s^-1
k5r=0.014;%s^-1
k6=0.13;%s^-1
k7=0.001;%s^-1
k7r=0.001;%s^-1
k8=0.13;%s^-1
k8r=0.13;%s^-1

%initial Concentrations
concE = 1e-8;
concP = 0;
concEM = 0;
concED = 0;
concM = 0;
concMext = 0;
concS = 1e-4;
concSext = 1e-4;
concD = 1e-8;
concDext = 1e-8;

%rate equations
rateP = @(M,P) (k3 * M + k4*P);
rateEM =@(S,E,M,EM) (k1 * S * E + k2r*E*M - k2*EM);
rateE = @(EM,E,M,S,D,ED) (k2*EM + K5r*ED - k1*S*E - k2r*E*M - K5*E*D);
rateS = @(S,Sext,E) (k1 * S * E + k7*Sext - k7r*S);
rateD = @(E,D,ED,Dext) (k8r*Dext - k8*D + k5r * ED - k5*E*D);
rateM = @(M,E,EM) ( k2*EM - k2r*E*M - k6*M - k3*M -k4*M);
rateED= @(E,D) (k5*E*D - k5r*ED);
rateSext=@(S,Sext) (k7*S - k7r * Sext);
rateDext=@(D,Dext) (k8*D - k8r * Dext);
rateMext=@(M) (k6*M);





