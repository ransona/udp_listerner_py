% Define the server address and port
serverAddress = '127.0.0.1';
serverPort = 5000;

% Create the UDP socket
udpSocket = udp(serverAddress, serverPort);
fopen(udpSocket);

% Set timeout period in seconds (10 minutes)
timeoutPeriod = 600;

% Send the 'mkdir' command
mkdirCommand = 'mkdir C:/Temp/abc';
fwrite(udpSocket, mkdirCommand);

% Wait for the response
startTime = tic; % Start timer
while udpSocket.BytesAvailable == 0
    elapsedTime = toc(startTime);
    if elapsedTime > timeoutPeriod
        error('Timeout: No response received from the server within 10 minutes.');
    end
    pause(0.1); % Short pause to avoid busy waiting
end

% Read and process the response
response = fread(udpSocket, udpSocket.BytesAvailable);
responseStr = char(response');
if strcmp(responseStr, '1')
    disp('mkdir Command succeeded.');
elseif strcmp(responseStr, '-1')
    disp('mkdir Command failed.');
else
    disp(['Unexpected server response: ', responseStr]);
end

% Send the 'sync' command
syncCommand = 'sync C:/Temp/abc C:/Temp/abc2';
fwrite(udpSocket, syncCommand);

% Wait for the response
startTime = tic; % Reset timer for the sync command
while udpSocket.BytesAvailable == 0
    elapsedTime = toc(startTime);
    if elapsedTime > timeoutPeriod
        error('Timeout: No response received from the server within 10 minutes.');
    end
    pause(0.1); % Short pause to avoid busy waiting
end

% Read and process the response
response = fread(udpSocket, udpSocket.BytesAvailable);
responseStr = char(response');
if strcmp(responseStr, '1')
    disp('sync Command succeeded.');
elseif strcmp(responseStr, '-1')
    disp('sync Command failed.');
else
    disp(['Unexpected server response: ', responseStr]);
end

% Close the UDP socket
fclose(udpSocket);
delete(udpSocket);
clear udpSocket;
