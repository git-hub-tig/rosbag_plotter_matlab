function plot_rosbag(full_path)

if ~ exist('full_path','var')
[file,path]= uigetfile('*.bag');
full_path=fullfile(path,file);
end

bag=rosbag(full_path);
display(bag.AvailableTopics(:,1:2));

choice = input("Enter the topic number  ");
topic=char(bag.AvailableTopics.Properties.RowNames(choice));

bagSelTopic = select(bag,'Topic',topic);

topictype=char(bag.AvailableTopics{choice,2});
pointMsg = rosmessage(topictype);
showdetails(pointMsg);

valid=0;

while ~ valid
    param=input("Enter the parameter  ",'s');
    try
        ts=timeseries(bagSelTopic,param);
        valid=1;
    catch
        warning(strcat(param,' is not valid')); 
    end
end

time=ts.Time-ts.Time(1);
data=ts.Data;

full_topic=strcat(topic,'/',strrep(lower(param),'.','/'));
y_label_input=input('Enter the y label name,unit (Enclose within codes) ');
y_label_splitted=regexp(y_label_input,',','split');

plot(time,data)
title(full_topic,'Interpreter','None')
xlabel('Time (in seconds)')
ylabel(strcat(y_label_splitted(1,1),' (in',{' '},y_label_splitted(1,2),')'))
xlim([0 max(time)])
legend(full_topic,'Interpreter','None')

end