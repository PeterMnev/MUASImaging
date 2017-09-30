%% Script 2 Text 

%% Standard Target

number=input('Enter target number:        ');

out=jsonencode(containers.Map({'alphanumeric','alphanumeric_color','background_color','latitude','longitude','orientation','shape','type'}, 
{input('Enter alphanumeric letter inside apostrophes:        '),
input('Enter alphanumeric color inside apostrophes:        '), 
input('Enter background color inside apostrophes:        '),
input('Enter latitude:        '), 
input('Enter longitude:        '),
input('Enter orientation:        '),
input('Enter shape:        '), 
'standard'}));



fileID = fopen(strcat(mat2str(number),'.json'),'w');

fprintf(fileID,out);

fclose(fileID);



%% Off Axis

number=input('Enter target number:        ');

out=jsonencode(containers.Map({'alphanumeric','alphanumeric_color','background_color','orientation','shape','type'}, ...

    {input('Enter alphanumeric letter inside apostrophes:        '),...

    input('Enter alphanumeric color inside apostrophes:        '), ...

    input('Enter background color inside apostrophes:        '), ...

    input('Enter orientation:        '), ...

    input('Enter shape:        '), ...

    'off_axis'}));



fileID = fopen(strcat(mat2str(number),'.json'),'w');

fprintf(fileID,out);

fclose(fileID);

%% Emergent

number=input('Enter target number:        ');

out=jsonencode(containers.Map({'description','latitude','longitude','type'}, ...

    {input('Enter description in single apostropes:           '), ...

    input('Enter latitude:        '), ...

    input('Enter longitude:        '), ...

    'emergent'}));



fileID = fopen(strcat(mat2str(number),'.json'),'w');

fprintf(fileID,out);

fclose(fileID);